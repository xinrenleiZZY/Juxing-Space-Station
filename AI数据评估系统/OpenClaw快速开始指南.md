# OpenClaw框架快速开始指南

## 一、环境准备

### 1.1 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装OpenClaw和相关依赖
pip install openclaw
pip install chromadb
pip install sentence-transformers
pip install fastapi uvicorn
pip install python-multipart
pip install pymongo
pip install psycopg2-binary
pip install python-dotenv
```

### 1.2 环境变量配置

创建 `.env` 文件：

```env
# 火山引擎API配置
VOLCANO_ENGINE_API_KEY=your_api_key_here
VOLCANO_ENGINE_MODEL=doubao-1-5-pro-32k-250115

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/dataip
MONGODB_URL=mongodb://localhost:27017/dataip
CHROMADB_HOST=localhost
CHROMADB_PORT=8000

# 文件存储配置
UPLOAD_DIR=./uploads
VECTOR_DB_DIR=./data/vectors
```

## 二、基础配置

### 2.1 初始化OpenClaw

```python
# config.py
from openclaw import OpenClawConfig
from openclaw.llms import VolcanoEngineLLM
from openclaw.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenClaw配置
    OPENCLAW_CONFIG = OpenClawConfig(
        llm=VolcanoEngineLLM(
            api_key=os.getenv("VOLCANO_ENGINE_API_KEY"),
            model=os.getenv("VOLCANO_ENGINE_MODEL")
        ),
        embedding=HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        ),
        vector_db={
            "type": "chromadb",
            "host": os.getenv("CHROMADB_HOST"),
            "port": int(os.getenv("CHROMADB_PORT", "8000"))
        }
    )
    
    # 文件存储配置
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./data/vectors")
    
    # 数据库配置
    DATABASE_URL = os.getenv("DATABASE_URL")
    MONGODB_URL = os.getenv("MONGODB_URL")

config = Config()
```

### 2.2 初始化向量数据库

```python
# vector_store.py
import chromadb
from chromadb.config import Settings
from openclaw import VectorStore
from config import config

class VectorStoreManager:
    def __init__(self):
        # 初始化ChromaDB客户端
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=config.VECTOR_DB_DIR,
                anonymized_telemetry=False
            )
        )
        
        # 创建集合
        self.collections = {
            "knowledge": self.client.get_or_create_collection(
                name="data_ip_knowledge",
                metadata={"hnsw:space": "cosine"}
            ),
            "cases": self.client.get_or_create_collection(
                name="evaluation_cases",
                metadata={"hnsw:space": "cosine"}
            ),
            "laws": self.client.get_or_create_collection(
                name="laws_regulations",
                metadata={"hnsw:space": "cosine"}
            )
        }
    
    def get_collection(self, name: str):
        return self.collections.get(name)

# 全局实例
vector_store_manager = VectorStoreManager()
```

## 三、文档处理模块

### 3.1 文档解析器

```python
# document_processor.py
from openclaw import DocumentProcessor
from openclaw.parsers import PDFParser, WordParser, CSVParser, TextParser
import os
from typing import Dict, List
from config import config

class DataIPDocumentProcessor:
    def __init__(self):
        self.processor = DocumentProcessor()
        
        # 注册解析器
        self.parsers = {
            '.pdf': PDFParser(),
            '.docx': WordParser(),
            '.doc': WordParser(),
            '.csv': CSVParser(),
            '.txt': TextParser(),
            '.json': TextParser(),
            '.xlsx': CSVParser(),
            '.xls': CSVParser()
        }
    
    async def process_document(self, file_path: str, metadata: Dict) -> Dict:
        """
        处理文档并提取关键信息
        """
        # 1. 获取文件扩展名
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 2. 选择合适的解析器
        parser = self.parsers.get(file_ext)
        if not parser:
            raise ValueError(f"不支持的文件格式: {file_ext}")
        
        # 3. 解析文档
        documents = await parser.parse(file_path)
        
        # 4. 提取关键信息
        extracted_info = self.extract_key_info(documents, metadata)
        
        # 5. 分块处理
        chunks = self.processor.chunk_documents(
            documents,
            chunk_size=500,
            overlap=50
        )
        
        # 6. 向量化存储
        from vector_store import vector_store_manager
        collection = vector_store_manager.get_collection("knowledge")
        
        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk.content],
                metadatas=[{
                    **metadata,
                    "chunk_id": i,
                    "source": file_path
                }],
                ids=[f"{metadata.get('document_id')}_{i}"]
            )
        
        return extracted_info
    
    def extract_key_info(self, documents: List, metadata: Dict) -> Dict:
        """
        提取关键信息
        """
        # 合并所有文档内容
        full_text = "\n".join([doc.content for doc in documents])
        
        # 提取关键信息
        extracted_info = {
            "total_length": len(full_text),
            "line_count": full_text.count('\n'),
            "word_count": len(full_text.split()),
            "has_numbers": any(char.isdigit() for char in full_text),
            "has_dates": self.detect_dates(full_text),
            "has_personal_info": self.detect_personal_info(full_text)
        }
        
        return extracted_info
    
    def detect_dates(self, text: str) -> bool:
        """检测是否包含日期"""
        import re
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{4}/\d{2}/\d{2}',
            r'\d{4}年\d{1,2}月\d{1,2}日'
        ]
        return any(re.search(pattern, text) for pattern in date_patterns)
    
    def detect_personal_info(self, text: str) -> bool:
        """检测是否包含个人信息"""
        import re
        patterns = [
            r'\d{17}[\dXx]',  # 身份证号
            r'1[3-9]\d{9}',   # 手机号
            r'[\w\.-]+@[\w\.-]+\.\w+'  # 邮箱
        ]
        return any(re.search(pattern, text) for pattern in patterns)

# 全局实例
document_processor = DataIPDocumentProcessor()
```

## 四、Agent智能体实现

### 4.1 数据评估Agent

```python
# agents/evaluation_agent.py
from openclaw import Agent, Tool
from openclaw.llms import VolcanoEngineLLM
from typing import Dict, Optional
import json

class DataEvaluationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="数据知识产权评估专家",
            llm=VolcanoEngineLLM(
                model="doubao-1-5-pro-32k-250115",
                temperature=0.3
            ),
            system_prompt=self.get_system_prompt()
        )
    
    def get_system_prompt(self):
        return """
你是一个专业的数据知识产权评估专家。你的职责是根据数据知识产权评估指标体系，对数据进行全面评估。

评估指标体系：

一、数据质量评估（30分）
1. 完整性（8分）：关键字段缺失率 ≤5%得8分，5%-20%得4分，>20%得0-2分
2. 准确性（7分）：数据真实可验证得7分，部分模糊/无法验证得3分，明显错误得0分
3. 规范性（6分）：格式统一、字段清晰得6分，格式较乱但可整理得3分，无结构得0分
4. 唯一性（4分）：已去重得4分，重复率<10%得2分，重复严重得0分
5. 可追溯性（5分）：来源、采集时间、更新记录完整得5分，部分可追溯得2分，完全无记录得0分

二、数据价值评估（25分）
1. 稀缺性（6分）：行业独有/难以获取得6分，较稀缺得3分，公开通用数据得1分
2. 时效性（5分）：实时/月度更新得5分，季度/年度更新得3分，多年不更新得1分
3. 应用场景（6分）：可用于生产/风控/定价/决策得6分，仅参考得3分，无明确用途得0分
4. 行业重要性（4分）：核心生产/经营数据得4分，辅助数据得2分，无关紧要得0分
5. 可变现潜力（4分）：可直接交易/赋能业务得4分，间接有用得2分，无变现可能得0分

三、合规与合法性评估（25分）
1. 数据来源合法（8分）：合法采集/授权/自有得8分，灰色来源得3分，非法爬取/窃取得0分
2. 隐私合规（7分）：无个人信息/已脱敏得7分，少量个人信息但可控得3分，大量隐私未脱敏得0分
3. 权属清晰（5分）：企业100%自有得5分，共同所有得2分，权属不清得0分
4. 数据安全措施（3分）：有存储/备份/权限得3分，简单存储得1分，无任何安全管理得0分
5. 无侵权纠纷（2分）：无纠纷得2分，潜在争议得0分

四、确权可行性评估（20分）
1. 独创性/加工深度（7分）：经过清洗、筛选、整合、特征工程得7分，简单整理得3分，原始搬运得0分
2. 数据成果化程度（5分）：形成数据集/数据产品/数据模型得5分，零散数据得2分
3. 登记通过率预判（4分）：高得4分，中得2分，低得0分
4. 可维护性与长期价值（4分）：可持续更新维护得4分，一次性数据得1分

评分等级：
AAA级（85-100分）：高价值、高质量、高通过率
AA级（70-84分）：优质数据
A级（55-69分）：可确权
B级（40-54分）：一般
C级（0-39分）：不建议申请

请根据提供的数据信息，严格按照评估指标体系进行评分，并给出详细的评分理由和建议。
"""
    
    @Tool
    def evaluate_quality(self, data_info: Dict) -> Dict:
        """
        数据质量评估工具
        """
        prompt = f"""
请根据以下数据信息，评估数据质量（总分30分）：

数据信息：
{json.dumps(data_info, ensure_ascii=False, indent=2)}

请按照以下维度评分：
1. 完整性（8分）
2. 准确性（7分）
3. 规范性（6分）
4. 唯一性（4分）
5. 可追溯性（5分）

请以JSON格式返回评分结果，包含每个维度的得分、总分和评分理由。
"""
        response = self.llm.generate(prompt)
        return json.loads(response)
    
    @Tool
    def evaluate_value(self, data_info: Dict) -> Dict:
        """
        数据价值评估工具
        """
        prompt = f"""
请根据以下数据信息，评估数据价值（总分25分）：

数据信息：
{json.dumps(data_info, ensure_ascii=False, indent=2)}

请按照以下维度评分：
1. 稀缺性（6分）
2. 时效性（5分）
3. 应用场景（6分）
4. 行业重要性（4分）
5. 可变现潜力（4分）

请以JSON格式返回评分结果，包含每个维度的得分、总分和评分理由。
"""
        response = self.llm.generate(prompt)
        return json.loads(response)
    
    @Tool
    def evaluate_compliance(self, data_info: Dict) -> Dict:
        """
        合规与合法性评估工具
        """
        prompt = f"""
请根据以下数据信息，评估合规与合法性（总分25分）：

数据信息：
{json.dumps(data_info, ensure_ascii=False, indent=2)}

请按照以下维度评分：
1. 数据来源合法（8分）
2. 隐私合规（7分）
3. 权属清晰（5分）
4. 数据安全措施（3分）
5. 无侵权纠纷（2分）

请以JSON格式返回评分结果，包含每个维度的得分、总分和评分理由。
"""
        response = self.llm.generate(prompt)
        return json.loads(response)
    
    @Tool
    def evaluate_ownership(self, data_info: Dict) -> Dict:
        """
        确权可行性评估工具
        """
        prompt = f"""
请根据以下数据信息，评估确权可行性（总分20分）：

数据信息：
{json.dumps(data_info, ensure_ascii=False, indent=2)}

请按照以下维度评分：
1. 独创性/加工深度（7分）
2. 数据成果化程度（5分）
3. 登记通过率预判（4分）
4. 可维护性与长期价值（4分）

请以JSON格式返回评分结果，包含每个维度的得分、总分和评分理由。
"""
        response = self.llm.generate(prompt)
        return json.loads(response)
    
    async def evaluate(self, data_info: Dict, file_content: Optional[str] = None) -> Dict:
        """
        执行完整评估
        """
        # 如果有文件内容，添加到数据信息中
        if file_content:
            data_info['file_content_preview'] = file_content[:1000]
        
        # 执行四大维度评估
        quality_result = await self.evaluate_quality(data_info)
        value_result = await self.evaluate_value(data_info)
        compliance_result = await self.evaluate_compliance(data_info)
        ownership_result = await self.evaluate_ownership(data_info)
        
        # 计算综合得分
        total_score = (
            quality_result.get('total_score', 0) +
            value_result.get('total_score', 0) +
            compliance_result.get('total_score', 0) +
            ownership_result.get('total_score', 0)
        )
        
        # 生成评估等级
        grade = self.calculate_grade(total_score)
        
        # 生成完整报告
        report = {
            "data_info": data_info,
            "quality_evaluation": quality_result,
            "value_evaluation": value_result,
            "compliance_evaluation": compliance_result,
            "ownership_evaluation": ownership_result,
            "total_score": total_score,
            "grade": grade,
            "recommendations": self.generate_recommendations(
                quality_result,
                value_result,
                compliance_result,
                ownership_result
            )
        }
        
        return report
    
    def calculate_grade(self, total_score: float) -> str:
        """
        计算评估等级
        """
        if total_score >= 85:
            return "AAA"
        elif total_score >= 70:
            return "AA"
        elif total_score >= 55:
            return "A"
        elif total_score >= 40:
            return "B"
        else:
            return "C"
    
    def generate_recommendations(self, quality, value, compliance, ownership):
        """
        生成优化建议
        """
        recommendations = []
        
        # 质量建议
        if quality.get('total_score', 0) < 20:
            recommendations.append("建议进行数据清洗和质量提升")
        
        # 价值建议
        if value.get('total_score', 0) < 15:
            recommendations.append("建议拓展数据应用场景，提升数据价值")
        
        # 合规建议
        if compliance.get('total_score', 0) < 15:
            recommendations.append("建议完善数据合规措施，确保数据来源合法")
        
        # 确权建议
        if ownership.get('total_score', 0) < 12:
            recommendations.append("建议加强数据加工处理，提升数据独创性")
        
        return recommendations

# 全局实例
evaluation_agent = DataEvaluationAgent()
```

### 4.2 智能问答Agent

```python
# agents/qa_agent.py
from openclaw import Agent, RAGRetriever
from openclaw.memory import ConversationBufferMemory
from openclaw.llms import VolcanoEngineLLM
from typing import List, Dict, Optional
from vector_store import vector_store_manager

class QAAgent(Agent):
    def __init__(self):
        super().__init__(
            name="数据知识产权问答专家",
            llm=VolcanoEngineLLM(
                model="doubao-1-5-pro-32k-250115",
                temperature=0.7
            ),
            memory=ConversationBufferMemory(memory_key="chat_history"),
            system_prompt=self.get_system_prompt()
        )
        
        # 初始化检索器
        self.retriever = RAGRetriever(
            vector_store=vector_store_manager.get_collection("knowledge"),
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 10}
        )
    
    def get_system_prompt(self):
        return """
你是一个专业的数据知识产权问答专家。你的职责是基于知识库和专业知识，回答用户关于数据知识产权的问题。

回答要求：
1. 准确性：确保回答准确、专业
2. 完整性：提供完整的答案，必要时引用相关法规和标准
3. 友好性：用通俗易懂的语言解释专业概念
4. 实用性：提供可操作的建议和指导

如果问题超出你的知识范围，请诚实告知用户。
"""
    
    async def chat(self, question: str, context: Optional[Dict] = None) -> Dict:
        """
        多轮对话问答
        """
        # 1. 检索相关知识
        relevant_docs = await self.retriever.retrieve(question)
        
        # 2. 构建提示词
        prompt = self.build_prompt(question, relevant_docs, context)
        
        # 3. 调用LLM生成答案
        response = await self.llm.generate(prompt)
        
        # 4. 保存对话历史
        self.memory.save_context(
            {"question": question},
            {"answer": response}
        )
        
        # 5. 返回结果
        return {
            "answer": response,
            "sources": self.format_sources(relevant_docs),
            "conversation_history": self.memory.load_memory_variables({})
        }
    
    def build_prompt(self, question: str, relevant_docs: List, context: Optional[Dict]) -> str:
        """
        构建提示词
        """
        # 格式化相关文档
        docs_text = "\n\n".join([
            f"【文档{i+1}】\n{doc.content}"
            for i, doc in enumerate(relevant_docs)
        ])
        
        # 构建上下文
        context_text = ""
        if context:
            context_text = f"\n当前评估数据信息：\n{context.get('data_info', {})}\n"
        
        prompt = f"""
{self.system_prompt}

相关知识：
{docs_text}

{context_text}

用户问题：{question}

请提供专业、准确的回答。
"""
        return prompt
    
    def format_sources(self, docs: List) -> List[Dict]:
        """
        格式化引用来源
        """
        return [
            {
                "content": doc.content[:200] + "...",
                "metadata": doc.metadata
            }
            for doc in docs
        ]

# 全局实例
qa_agent = QAAgent()
```

## 五、FastAPI后端实现

### 5.1 主应用

```python
# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import shutil
from datetime import datetime

from config import config
from document_processor import document_processor
from agents.evaluation_agent import evaluation_agent
from agents.qa_agent import qa_agent

app = FastAPI(
    title="数据知识产权评估系统",
    description="基于OpenClaw框架的数据知识产权评估RAG系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保上传目录存在
os.makedirs(config.UPLOAD_DIR, exist_ok=True)

# 数据模型
class UploadResponse(BaseModel):
    document_id: str
    status: str
    message: str

class EvaluationRequest(BaseModel):
    document_id: str
    additional_info: Optional[dict] = None

class EvaluationResponse(BaseModel):
    evaluation_id: str
    total_score: float
    grade: str
    report: dict

class ChatRequest(BaseModel):
    question: str
    document_id: Optional[str] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    conversation_id: str

# 存储文档信息（实际应用中应使用数据库）
documents_db = {}
evaluations_db = {}

# API接口
@app.post("/api/documents/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    company_name: str = Form(...),
    data_name: str = Form(...),
    data_type: str = Form(...),
    data_scale: str = Form(...),
    data_source: str = Form(...),
    industry: str = Form(...)
):
    """
    上传数据文档
    """
    try:
        # 生成文档ID
        document_id = f"doc_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 保存文件
        file_path = os.path.join(config.UPLOAD_DIR, f"{document_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 保存文档信息
        documents_db[document_id] = {
            "file_path": file_path,
            "company_name": company_name,
            "data_name": data_name,
            "metadata": {
                "data_type": data_type,
                "data_scale": data_scale,
                "data_source": data_source,
                "industry": industry
            },
            "upload_time": datetime.now().isoformat(),
            "status": "uploaded"
        }
        
        return UploadResponse(
            document_id=document_id,
            status="uploaded",
            message="文档上传成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/evaluations/start", response_model=EvaluationResponse)
async def start_evaluation(request: EvaluationRequest):
    """
    启动数据评估
    """
    try:
        # 获取文档信息
        document = documents_db.get(request.document_id)
        if not document:
            raise HTTPException(status_code=404, detail="文档不存在")
        
        # 读取文件内容
        with open(document["file_path"], "r", encoding="utf-8") as f:
            file_content = f.read()
        
        # 准备数据信息
        data_info = {
            "company_name": document["company_name"],
            "data_name": document["data_name"],
            **document["metadata"]
        }
        
        # 如果有额外信息，添加到数据信息中
        if request.additional_info:
            data_info.update(request.additional_info)
        
        # 执行评估
        report = await evaluation_agent.evaluate(data_info, file_content)
        
        # 生成评估ID
        evaluation_id = f"eval_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 保存评估结果
        evaluations_db[evaluation_id] = {
            "document_id": request.document_id,
            "report": report,
            "evaluation_time": datetime.now().isoformat()
        }
        
        return EvaluationResponse(
            evaluation_id=evaluation_id,
            total_score=report["total_score"],
            grade=report["grade"],
            report=report
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    智能问答
    """
    try:
        # 准备上下文
        context = None
        if request.document_id:
            document = documents_db.get(request.document_id)
            if document:
                context = {
                    "data_info": {
                        "company_name": document["company_name"],
                        "data_name": document["data_name"],
                        **document["metadata"]
                    }
                }
        
        # 执行问答
        result = await qa_agent.chat(request.question, context)
        
        # 生成会话ID
        conversation_id = request.conversation_id or f"conv_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=conversation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/evaluations/{evaluation_id}")
async def get_evaluation(evaluation_id: str):
    """
    获取评估结果
    """
    evaluation = evaluations_db.get(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="评估结果不存在")
    
    return evaluation

@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 5.2 启动服务

```bash
# 启动后端服务
python main.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 六、测试示例

### 6.1 上传文档测试

```python
import requests

# 上传文档
url = "http://localhost:8000/api/documents/upload"
files = {"file": open("test_data.csv", "rb")}
data = {
    "company_name": "测试公司",
    "data_name": "销售数据",
    "data_type": "交易数据",
    "data_scale": "100万条",
    "data_source": "企业自有",
    "industry": "零售业"
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

### 6.2 评估测试

```python
# 启动评估
url = "http://localhost:8000/api/evaluations/start"
data = {
    "document_id": "doc_20260227120000",
    "additional_info": {
        "data_description": "包含2023年全年销售数据"
    }
}

response = requests.post(url, json=data)
print(response.json())
```

### 6.3 问答测试

```python
# 智能问答
url = "http://localhost:8000/api/chat"
data = {
    "question": "数据知识产权评估需要哪些条件？",
    "document_id": "doc_20260227120000"
}

response = requests.post(url, json=data)
print(response.json())
```

## 七、下一步优化

### 7.1 添加数据库持久化

```python
# 使用PostgreSQL和MongoDB存储数据
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

# PostgreSQL连接
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# MongoDB连接
mongo_client = MongoClient(config.MONGODB_URL)
mongo_db = mongo_client["dataip"]
```

### 7.2 添加用户认证

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
```

### 7.3 添加异步任务处理

```python
from celery import Celery

celery_app = Celery('dataip', broker='redis://localhost:6379/0')

@celery_app.task
async def process_document_task(document_id: str):
    """
    异步处理文档任务
    """
    document = documents_db.get(document_id)
    if document:
        await document_processor.process_document(
            document["file_path"],
            document["metadata"]
        )
```

---

**文档版本**: v1.0  
**创建日期**: 2026-02-27  
**更新日期**: 2026-02-27