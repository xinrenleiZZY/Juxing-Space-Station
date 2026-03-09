using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Newtonsoft.Json;
using MarkdownSharp;

namespace AIChatWPF
{
    public partial class MainWindow : Window
    {
        private readonly HttpClient _httpClient;
        private readonly Markdown _markdown;
        private readonly string _apiKey = "a3e3e754-162c-4bf3-b9b6-7519784e4f00";
        private readonly string _apiUrl = "https://api.deepseek.com/v1/chat/completions";
        private string _conversationHtml = "";

        public MainWindow()
        {
            InitializeComponent();
            _httpClient = new HttpClient();
            _markdown = new Markdown();
            InitializeWebView();
        }

        private async void InitializeWebView()
        {
            await ChatWebView.EnsureCoreWebView2Async();
            UpdateChatDisplay();
        }

        private void UpdateChatDisplay()
        {
            string html = $@"
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <style>
        body {{
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background-color: #1a1a2e;
            color: #eaeaea;
            padding: 20px;
            margin: 0;
            line-height: 1.6;
        }}
        .message {{
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 12px;
            max-width: 85%;
        }}
        .user-message {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin-left: auto;
            color: white;
        }}
        .assistant-message {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-right: auto;
        }}
        .message-header {{
            font-size: 12px;
            color: rgba(255, 255, 255, 0.6);
            margin-bottom: 8px;
        }}
        .message-content {{
            font-size: 14px;
        }}
        .message-content h1, .message-content h2, .message-content h3 {{
            color: #eaeaea;
            margin: 10px 0;
        }}
        .message-content h1 {{
            font-size: 1.5em;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 5px;
        }}
        .message-content h2 {{
            font-size: 1.3em;
        }}
        .message-content h3 {{
            font-size: 1.1em;
        }}
        .message-content p {{
            margin: 8px 0;
        }}
        .message-content ul, .message-content ol {{
            margin: 8px 0;
            padding-left: 20px;
        }}
        .message-content li {{
            margin: 4px 0;
        }}
        .message-content code {{
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
            font-size: 0.9em;
        }}
        .message-content pre {{
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
        }}
        .message-content pre code {{
            background: transparent;
            padding: 0;
        }}
        .message-content blockquote {{
            border-left: 3px solid #667eea;
            margin: 10px 0;
            padding-left: 15px;
            color: rgba(255, 255, 255, 0.8);
        }}
        .message-content strong {{
            color: #667eea;
        }}
        .message-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        .message-content th, .message-content td {{
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px;
            text-align: left;
        }}
        .message-content th {{
            background: rgba(102, 126, 234, 0.2);
        }}
        .system-message {{
            background: rgba(102, 126, 234, 0.1);
            border: 1px solid rgba(102, 126, 234, 0.3);
            text-align: center;
            max-width: 100%;
        }}
    </style>
</head>
<body>
    <div class='message system-message'>
        <div class='message-content'>
            <p>👋 你好！我是AI智能助手。我可以帮你解答各种问题，包括：</p>
            <ul>
                <li>数据知识产权评估相关问题</li>
                <li>技术咨询和代码问题</li>
                <li>数据分析和处理建议</li>
                <li>其他专业问题</li>
            </ul>
            <p>请在下方输入你的问题，我会尽力为你提供专业的回答。</p>
        </div>
    </div>
    {_conversationHtml}
</body>
</html>";

            ChatWebView.NavigateToString(html);
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            await SendMessage();
        }

        private async void QuestionTextBox_KeyDown(object sender, KeyEventArgs e)
        {
            // 按Enter发送，Shift+Enter换行
            if (e.Key == Key.Enter && !Keyboard.IsKeyDown(Key.LeftShift) && !Keyboard.IsKeyDown(Key.RightShift))
            {
                e.Handled = true;
                await SendMessage();
            }
        }

        private async Task SendMessage()
        {
            string question = QuestionTextBox.Text.Trim();
            if (string.IsNullOrEmpty(question))
                return;

            // 获取选中的模型
            var selectedItem = ModelComboBox.SelectedItem as ComboBoxItem;
            string modelId = selectedItem?.Tag?.ToString() ?? "deepseek-v3-250324";

            // 添加用户消息到对话
            AddUserMessage(question);
            QuestionTextBox.Clear();

            // 显示加载状态
            SetLoadingState(true);

            try
            {
                string answer = await CallAIAPI(question, modelId);
                AddAssistantMessage(answer);
            }
            catch (Exception ex)
            {
                AddAssistantMessage($"抱歉，发生了错误：{ex.Message}");
            }
            finally
            {
                SetLoadingState(false);
            }
        }

        private async Task<string> CallAIAPI(string question, string modelId)
        {
            var requestData = new
            {
                model = modelId,
                messages = new[]
                {
                    new
                    {
                        role = "system",
                        content = "你是一个专业的助手，回答必须使用清晰规范的 Markdown 格式：分段用换行，标题用 # 层级，列表用 - 或 1.，代码用 ``` 包裹，重点内容用 ** 加粗，不要多余符号，确保输出能直接渲染。"
                    },
                    new
                    {
                        role = "user",
                        content = question
                    }
                },
                temperature = 0.7,
                stream = false
            };

            var json = JsonConvert.SerializeObject(requestData);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            _httpClient.DefaultRequestHeaders.Clear();
            _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_apiKey}");

            var response = await _httpClient.PostAsync(_apiUrl, content);
            response.EnsureSuccessStatusCode();

            var responseJson = await response.Content.ReadAsStringAsync();
            dynamic result = JsonConvert.DeserializeObject(responseJson);

            if (result.choices != null && result.choices.Count > 0)
            {
                return result.choices[0].message.content.ToString();
            }

            return "抱歉，未能获取到回答。";
        }

        private void AddUserMessage(string message)
        {
            string escapedMessage = System.Web.HttpUtility.HtmlEncode(message);
            _conversationHtml += $@"
    <div class='message user-message'>
        <div class='message-header'>你</div>
        <div class='message-content'>{escapedMessage}</div>
    </div>";
            UpdateChatDisplay();
        }

        private void AddAssistantMessage(string message)
        {
            // 将Markdown转换为HTML
            string htmlContent = _markdown.Transform(message);
            _conversationHtml += $@"
    <div class='message assistant-message'>
        <div class='message-header'>AI助手</div>
        <div class='message-content'>{htmlContent}</div>
    </div>";
            UpdateChatDisplay();
        }

        private void SetLoadingState(bool isLoading)
        {
            SendButton.IsEnabled = !isLoading;
            QuestionTextBox.IsEnabled = !isLoading;
            LoadingProgressBar.Visibility = isLoading ? Visibility.Visible : Visibility.Collapsed;
        }

        protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
        {
            _httpClient?.Dispose();
            base.OnClosing(e);
        }
    }
}