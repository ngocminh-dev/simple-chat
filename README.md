Note:

1. Start LM Studio, load model and start sever
2. Open code in Dev Container
3. Run
   Backend:
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

Frontend:
cd frontend
npm run dev -- --host 0.0.0.0
