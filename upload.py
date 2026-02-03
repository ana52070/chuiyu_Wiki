import os
import subprocess
import sys
import datetime

# ================= 配置区域 =================
# 如果你的梯子端口是 7890 (Clash常见端口)，请修改这里
# 如果不需要代理，设置为 None
PROXY_PORT = "7897"  
REMOTE_REPO = "origin"
BRANCH = "main"
# ===========================================

def run_command(command, use_proxy=False):
    """运行系统命令，支持代理设置"""
    env = os.environ.copy()
    
    if use_proxy and PROXY_PORT:
        proxy_url = f"http://127.0.0.1:{PROXY_PORT}"
        print(f"🔌 使用代理: {proxy_url}")
        env["http_proxy"] = proxy_url
        env["https_proxy"] = proxy_url
        env["ALL_PROXY"] = f"socks5://127.0.0.1:{PROXY_PORT}"

    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 错误: {e.stderr}")
        return False

def git_sync():
    print("🚀 开始同步知识库...")
    
    # 1. Git Add
    print("Stage 1: 添加文件 (git add)...")
    if not run_command("git add ."): return

    # 2. Git Commit
    # 获取当前时间作为默认 commit 信息，或者从命令行参数获取
    commit_msg = f"Auto update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    
    print(f"Stage 2: 提交更改 (git commit) -> '{commit_msg}'...")
    # 允许 commit 为空（如果没有变化）
    run_command(f'git commit -m "{commit_msg}"')

    # 3. Git Push (关键步骤)
    print("Stage 3: 推送到云端 (git push)...")
    
    # 先尝试直连
    print("   Trying direct connection...")
    success = run_command(f"git push {REMOTE_REPO} {BRANCH}")
    
    # 如果直连失败且配置了代理，尝试走代理
    if not success and PROXY_PORT:
        print("\n⚠️ 直连失败，尝试切换代理通道重试...")
        success = run_command(f"git push {REMOTE_REPO} {BRANCH}", use_proxy=True)
    
    if success:
        print("\n✅ 同步成功！你的知识库已更新。")
    else:
        print("\n❌ 同步失败，请检查网络或 Git 配置。")

if __name__ == "__main__":
    git_sync()