## 開発者向け情報

### テスト実行

```bash
uv run pytest
```

### リンター実行

```bash
uv run ruff check .
```

## 配布

事前に PyPI アカウントを作成し、`~/.pypirc`に以下を記述。

```
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository: https://upload.pypi.org/legacy/
username: __token__
password: <APIキー>

[pypitest]
repository: https://test.pypi.org/legacy/
username: __token__
password: <APIキー>
```

```bash
# 事前にテストを実行
uv run pytest

# 事前にpyproject.tomlのversionを更新
cat pyproject.toml

# 古いビルド成果物を削除
rm -rf dist/
rm -rf build/
rm -rf middleman_ai.egg-info/

# 設定が正しいか事前チェック
uv run python setup.py check

# ビルド
uv run python setup.py sdist
uv run python setup.py bdist_wheel

# descriptionの形式が正しいかチェック
uv run twine check dist/*

# 配信
uv run twine upload --repository pypitest dist/* # テスト用
uv run twine upload --repository pypi dist/* # 本番用
```
