# realearn-evidence

realearn（realearn.online）的**公开实跑证据数据集**——每个教程里出现的终端输出，都在这里以结构化 JSON 形式可引用、可复现。

## 数据口径

- **零编造**：每条 `command` / `output` 逐字来自 realearn 内部 lab 记录（`labs/labNN/evidence.json` 的 `source_record` 字段指向原始 markdown）。
- **未记录即 null**：原始 lab 记录未记的 `output_exit_code` 等字段如实置 `null`，绝不补造。
- **subject_sha256**：分析对象的内容寻址。2026-10-16 在同一实验机对全部保留产物重算 `sha256sum` 并与 lab 记录值核对一致（见各文件 `sha256_recomputed`）。
- **environment**：记录 OS / node / 编译器 / 工具链版本。同一实验机跑全部 lab。
- **verified_date**：数据导出并在原机复核的日期；`date` 为 lab 实跑日期。

## Schema

```json
{
  "dataset": "realearn-evidence",
  "schema_version": 1,
  "lab_id": "labNN",
  "date": "实跑日期",
  "verified_date": "导出复核日期",
  "source_record": "原始 lab 记录文件路径",
  "environment": { "os": "...", "node": "...", "workdir": "..." },
  "entries": [
    {
      "step": "步骤标识",
      "command": "终端命令（逐字）",
      "output": "终端输出（逐字）",
      "output_exit_code": 0 或 null（未记录）,
      "subject_sha256": "分析对象 sha256 或 null",
      "note": "补充说明（含授权依据）"
    }
  ],
  "sha256_recomputed": { "文件名": "sha256", "note": "..." }
}
```

## 目录

- `labs/lab00/` — REA 安装 + Hermes MCP 接入 + 环境诊断（含附录 R8-A：pwntools-elf 轻量引擎点亮、evidence bundle 闭环、能力边界）
- `labs/lab01/` — 第一个合法分析目标：自编译 hello ELF（gcc/-O0/readelf/objdump 三方对账）
- `labs/lab02/` — stripped 二进制与字符串证据（strip 后锚点定位、strings 扫描）
- `labs/lab03/` — 系统 OpenSSL libcrypto 只读分析（Apache-2.0 授权依据）

## 复现方法

1. Linux x86_64（记录环境：opencloudos 9.4，node v22.22.0，gcc + binutils 系统包）
2. `npm install rea-agents@6.4.0`（lab00）
3. `python3 -m venv .rea-python && .rea-python/bin/pip install pwntools==4.15.0 pyelftools==0.33 unicorn==2.1.2`（lab00 附录 R8-A）
4. lab01/02 目标为 5 行内自编译源码（源码与 sha256 见各 JSON 的 note / sha256_recomputed），自行编译后逐条重跑 `command` 字段即可对账。
5. lab03 分析对象为系统自带 OpenSSL（各发行版路径/版本可能不同；仅只读分析）。

## 合规

- 全部分析目标授权链完整：自编译产物（作者=分析者）或 Apache-2.0 开源二进制（license 明文允许反编译研究）。
- 本仓不含任何密钥、token、内网地址或非公开信息。

## License

数据集内容以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 发布；引用的 OpenSSL 等第三方事实不受本许可约束。
