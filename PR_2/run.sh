#!/bin/bash
export PATH=$HOME/.local/bin:$PATH

echo "=== Тестирование Этапа 5: Визуализация ==="

echo -e "\n1. Тестовый репозиторий (с циклическими зависимостями)"
python3 stage5.py --package A --url test_repo.json --test-mode --pkg-version 1.0.0 --output test_graph.svg --max-depth 5

echo -e "\n2. Реальный пакет 1 (express)"
python3 stage5.py --package express --url https://registry.npmjs.org --pkg-version 4.18.2 --output express_graph.svg --max-depth 1

echo -e "\n3. Реальный пакет 2 (chalk)"
python3 stage5.py --package chalk --url https://registry.npmjs.org --pkg-version 4.1.2 --output chalk_graph.svg --max-depth 2

echo -e "\n4. Реальный пакет 3 (lodash) - пакет без зависимостей"
python3 stage5.py --package lodash --url https://registry.npmjs.org --pkg-version 4.17.21 --output lodash_graph.svg --max-depth 1