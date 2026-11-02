@echo off
chcp 65001 >nul

echo === Тестирование Этапа 5: Визуализация ===

echo 1. Тестовый репозиторий (с циклическими зависимостями)
python stage5.py --package A --url test_repo.json --test-mode --pkg-version 1.0.0 --output test_graph.svg --max-depth 5
echo.

echo 2. Реальный пакет 1 (express)
python stage5.py --package express --url https://registry.npmjs.org --pkg-version 4.18.2 --output express_graph.svg --max-depth 1
echo.

echo 3. Реальный пакет 2 (chalk)
python stage5.py --package chalk --url https://registry.npmjs.org --pkg-version 4.1.2 --output chalk_graph.svg --max-depth 2
echo.

echo 4. Реальный пакет 3 (lodash) - пакет без зависимостей
python stage5.py --package lodash --url https://registry.npmjs.org --pkg-version 4.17.21 --output lodash_graph.svg --max-depth 1
echo.