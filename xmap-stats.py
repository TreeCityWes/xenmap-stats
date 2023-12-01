name: Run xmap-stats.py

on:
  push:
    branches:
      - main 

jobs:
  build:
    runs-on: ubuntu-latest  

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.x 

      - name: Install dependencies (if needed)
        run: |
          pip install -r ${{ github.workspace }}/requirements.txt  # Replace with the correct path to requirements.txt
        working-directory: ${{ github.workspace }}

      - name: Run xmap-stats.py
        run: |
          python xmap-stats.py
        working-directory: ${{ github.workspace }}  

      - name: Save CSV and JSON artifacts
        if: success()  
        run: |
          cp xenmaps_messages.csv ${{ github.workspace }}/xenmaps_messages.csv
          cp xenmaps.json ${{ github.workspace }}/xenmaps.json
        working-directory: ${{ github.workspace }}

      - name: Upload CSV and JSON artifacts
        if: success()  
        uses: actions/upload-artifact@v2
        with:
          name: xenmaps-artifacts
          path: xenmaps_messages.csv, xenmaps.json
