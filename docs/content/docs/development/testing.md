+++
title = "测试指南"
description = "编写和运行 biliup 项目的测试"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 70
template = "docs/page.html"

[extra]
lead = "本文档说明如何为 biliup 项目编写单元测试、集成测试，以及如何运行测试套件。"
toc = true
top = false
+++

## 测试框架

biliup 使用以下测试框架：

- **Rust**: cargo test
- **Python**: pytest
- **前端**: Jest + React Testing Library

## Rust 测试

### 单元测试

在源文件中编写单元测试：

```rust
// crates/biliup/src/uploader.rs

pub fn calculate_chunk_size(file_size: u64) -> u64 {
    if file_size < 100 * 1024 * 1024 {
        4 * 1024 * 1024  // 4MB
    } else {
        8 * 1024 * 1024  // 8MB
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_calculate_chunk_size_small_file() {
        let size = calculate_chunk_size(50 * 1024 * 1024);
        assert_eq!(size, 4 * 1024 * 1024);
    }
    
    #[test]
    fn test_calculate_chunk_size_large_file() {
        let size = calculate_chunk_size(200 * 1024 * 1024);
        assert_eq!(size, 8 * 1024 * 1024);
    }
}
```

### 集成测试

在 `tests/` 目录创建集成测试：

```rust
// crates/biliup/tests/upload_test.rs

use biliup::Uploader;

#[tokio::test]
async fn test_upload_video() {
    let uploader = Uploader::new("test_video.mp4");
    let result = uploader.upload().await;
    assert!(result.is_ok());
}
```

### 运行测试

```bash
# 运行所有测试
cargo test

# 运行特定测试
cargo test test_calculate_chunk_size

# 显示输出
cargo test -- --nocapture

# 运行特定 crate 的测试
cargo test -p biliup
```

## Python 测试

### 安装 pytest

```bash
pip install pytest pytest-asyncio pytest-cov
```

### 单元测试

```python
# tests/test_downloader.py

import pytest
from biliup.plugins.douyu import Douyu

@pytest.mark.asyncio
async def test_extract_room_id():
    """测试房间号提取"""
    downloader = Douyu(
        fname="test",
        url="https://www.douyu.com/123456"
    )
    
    room_id = downloader.extract_room_id()
    assert room_id == "123456"

@pytest.mark.asyncio
async def test_check_stream():
    """测试直播状态检查"""
    downloader = Douyu(
        fname="test",
        url="https://www.douyu.com/123456"
    )
    
    result = await downloader.acheck_stream(is_check=True)
    assert isinstance(result, bool)
```

### Mock 测试

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_room_info_with_mock():
    """使用 Mock 测试"""
    downloader = Douyu(
        fname="test",
        url="https://www.douyu.com/123456"
    )
    
    # Mock HTTP 请求
    with patch('biliup.common.util.client.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.text = '{"code":0,"data":{"is_live":true,"title":"测试"}}'
        mock_get.return_value = mock_response
        
        room_info = await downloader.get_room_info()
        assert room_info['is_live'] == True
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_downloader.py

# 运行特定测试
pytest tests/test_downloader.py::test_extract_room_id

# 显示详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=biliup --cov-report=html
```

## 前端测试

### 组件测试

```typescript
// app/ui/__tests__/Player.test.tsx

import { render, screen } from '@testing-library/react';
import Player from '../Player';

describe('Player', () => {
  it('renders video player', () => {
    render(<Player url="https://example.com/video.mp4" />);
    const player = screen.getByRole('video');
    expect(player).toBeInTheDocument();
  });
  
  it('displays error message on invalid URL', () => {
    render(<Player url="" />);
    const error = screen.getByText(/invalid url/i);
    expect(error).toBeInTheDocument();
  });
});
```

### API 测试

```typescript
// app/lib/__tests__/api.test.ts

import { getStats } from '../api';

global.fetch = jest.fn();

describe('API', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });
  
  it('fetches stats successfully', async () => {
    const mockStats = {
      total_downloads: 100,
      total_uploads: 50,
    };
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockStats,
    });
    
    const stats = await getStats();
    expect(stats).toEqual(mockStats);
  });
});
```

### 运行测试

```bash
# 运行所有测试
npm test

# 监听模式
npm test -- --watch

# 生成覆盖率报告
npm test -- --coverage
```

## 测试最佳实践

### 1. 测试命名

使用描述性的测试名称：

```python
# 好的命名
def test_extract_room_id_from_standard_url():
    pass

def test_extract_room_id_from_mobile_url():
    pass

# 不好的命名
def test1():
    pass

def test_room():
    pass
```

### 2. 测试隔离

每个测试应该独立：

```python
@pytest.fixture
def downloader():
    """为每个测试创建新的实例"""
    return Douyu(fname="test", url="https://www.douyu.com/123456")

def test_check_stream(downloader):
    # 使用 fixture
    result = await downloader.acheck_stream()
    assert result == True
```

### 3. 测试覆盖率

追求合理的测试覆盖率（70-80%）：

```bash
# Python
pytest --cov=biliup --cov-report=term-missing

# Rust
cargo tarpaulin --out Html
```

### 4. 持续集成

在 CI 中运行测试：

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Rust tests
        run: cargo test
      
      - name: Run Python tests
        run: pytest
      
      - name: Run frontend tests
        run: npm test
```

## 相关文档

- [调试技巧](./debugging.md)
- [源码编译](./building-from-source.md)
