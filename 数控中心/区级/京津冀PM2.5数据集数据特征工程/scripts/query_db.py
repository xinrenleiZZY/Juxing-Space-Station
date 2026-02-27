#!/usr/bin/env python
"""增强版数据库查看与交互脚本（REPL）

支持：
- list                列出数据库中所有表
- info <table>        显示表结构（PRAGMA table_info）
- sql <SQL>           执行 SQL 并返回全部结果（谨慎使用）
- show <SQL>          执行 SQL 并以分页方式显示结果
- export <SQL> <file> 执行 SQL 并导出结果到 CSV（若无文件则提示）
- next                在分页显示中显示下一页
- prev                在分页显示中显示上一页
- page <n>            跳到第 n 页
- size <n>            设置分页大小（默认 20）
- help                显示帮助
- exit / quit         退出

示例：
  python scripts\query_db.py --list
  python scripts\query_db.py    (进入交互模式)
"""
import sys
import os
import argparse
import shlex

# Ensure project root on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.data_processing import storage
import logging

# 使用 storage 中配置的 db_operations 日志
logger = logging.getLogger("db_operations")


class REPL:
    def __init__(self, page_size=20):
        self.page_size = page_size
        self.current_df = None
        self.current_sql = None
        self.page = 0

    def list_tables(self):
        tables = storage.list_tables()
        if not tables:
            print('数据库中未发现表。')
            return
        print('数据库表：')
        for t in tables:
            print(' -', t)

    def info(self, table):
        try:
            info = storage.table_info(table)
            if info is None or info.empty:
                print(f'未找到表 {table} 的结构信息')
                return
            print(info.to_string(index=False))
        except Exception as e:
            print('获取表结构失败：', e)
            logger.exception(f'获取表结构失败：{table} -> {e}')

    def run_sql(self, sql, store=False):
        try:
            df = storage.query_sqlite(sql)
        except Exception as e:
            print('查询失败：', e)
            logger.exception(f'查询失败：{sql} -> {e}')
            return None
        if df is None or df.empty:
            print('查询未返回数据')
            return df
        if store:
            self.current_df = df
            self.current_sql = sql
            self.page = 0
        return df

    def show(self, sql=None):
        if sql:
            df = self.run_sql(sql, store=True)
        else:
            df = self.current_df
        if df is None or df.empty:
            print('无可显示结果')
            return
        self._print_page()

    def export(self, sql, path):
        df = self.run_sql(sql, store=False)
        if df is None or df.empty:
            print('无数据可导出')
            return
        try:
            dirp = os.path.dirname(path) or '.'
            if dirp and not os.path.exists(dirp):
                os.makedirs(dirp, exist_ok=True)
            df.to_csv(path, index=False, encoding='utf-8-sig')
            print('已导出到：', path)
            logger.info(f'已导出查询结果到 CSV：{path}')
        except Exception as e:
            print('导出失败：', e)
            logger.exception(f'导出失败：{e}')

    def set_size(self, n):
        try:
            n = int(n)
            if n <= 0:
                raise ValueError()
            self.page_size = n
            self.page = 0
            print('分页大小已设置为', n)
        except Exception:
            print('分页大小无效')

    def next_page(self):
        if self.current_df is None:
            print('当前未加载数据')
            return
        max_page = (len(self.current_df) - 1) // self.page_size
        if self.page < max_page:
            self.page += 1
            self._print_page()
        else:
            print('已经是最后一页')

    def prev_page(self):
        if self.current_df is None:
            print('当前未加载数据')
            return
        if self.page > 0:
            self.page -= 1
            self._print_page()
        else:
            print('已经是第一页')

    def goto_page(self, n):
        try:
            n = int(n)
            if n < 1:
                raise ValueError()
            idx = n - 1
            max_page = (len(self.current_df) - 1) // self.page_size
            if idx > max_page:
                print('页码超出范围')
                return
            self.page = idx
            self._print_page()
        except Exception:
            print('页码无效')

    def _print_page(self):
        df = self.current_df
        start = self.page * self.page_size
        end = start + self.page_size
        sub = df.iloc[start:end]
        print(f'-- 第 {self.page+1} 页 （行 {start+1}-{min(end,len(df))} / 共 {len(df)} 行） --')
        print(sub.to_string(index=False))


def repl_loop(initial_list=False):
    r = REPL()
    if initial_list:
        r.list_tables()

    print('\n输入 "help" 查看命令列表。\n')
    while True:
        try:
            line = input('查询> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        parts = shlex.split(line)
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ('exit', 'quit'):
            break
        if cmd == 'help':
            print(__doc__)
            continue
        if cmd == 'list':
            r.list_tables()
            continue
        if cmd == 'info' and args:
            r.info(args[0]); continue
        if cmd == 'sql' and args:
            sql = line[len('sql'):].strip()
            r.run_sql(sql, store=False); continue
        if cmd == 'show':
            sql = line[len('show'):].strip()
            if sql:
                r.show(sql)
            else:
                r.show()
            continue
        if cmd == 'export' and len(args) >= 2:
            # export <SQL> <path>  -> SQL may contain spaces; assume last arg is path
            path = args[-1]
            sql = line[len('export'):].strip()
            # remove trailing path from sql
            if sql.endswith(path):
                sql = sql[: -len(path)].strip()
            r.export(sql, path)
            continue
        if cmd == 'next':
            r.next_page(); continue
        if cmd == 'prev':
            r.prev_page(); continue
        if cmd == 'page' and args:
            r.goto_page(args[0]); continue
        if cmd == 'size' and args:
            r.set_size(args[0]); continue
        print('未知命令。输入 "help" 查看命令。')


def main():
    parser = argparse.ArgumentParser(description="本地 AQI SQLite 数据库查询工具（支持交互REPL）")
    parser.add_argument('--list', action='store_true', help='列出所有表并退出')
    parser.add_argument('--info', metavar='TABLE', help='显示表结构并退出')
    parser.add_argument('--sql', metavar='SQL', help='执行 SQL 并打印结果后退出')
    parser.add_argument('--export', nargs=2, metavar=('SQL', 'PATH'), help='执行 SQL 并导出为 CSV，然后退出')
    args = parser.parse_args()

    if args.list:
        tables = storage.list_tables()
        if not tables:
            print('数据库中未发现表。')
            return
        print('数据库表：')
        for t in tables:
            print(' -', t)
        return

    if args.info:
        repl = REPL()
        repl.info(args.info)
        return

    if args.sql:
        # run SQL and print full result
        repl = REPL()
        df = repl.run_sql(args.sql, store=False)
        if df is not None and not df.empty:
            print(df.to_string(index=False))
        return

    if args.export:
        sql, path = args.export
        repl = REPL()
        repl.export(sql, path)
        return

    # no top-level args -> enter REPL
    repl_loop(initial_list=True)


if __name__ == '__main__':
    main()
