@echo off
echo ============================================================
echo PharmaDrishti - Model Retraining Script
echo ============================================================
echo.
echo This will retrain the model with:
echo - 5,000 medicines (up from 50)
echo - 500,000 interactions (up from 5,000)
echo - New terminology: Batch Price and Manufacturing Score
echo.
echo Expected training time: 3-8 minutes
echo.
pause
echo.
echo Starting training...
echo.
python train_model.py
echo.
echo ============================================================
echo Training Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Check models/ folder for new model files
echo 2. Run dashboard: streamlit run dashboard.py
echo 3. Test with new batch pricing and manufacturing score
echo.
pause
