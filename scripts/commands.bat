@echo off
REM =========================
REM 1. Deploy MongoDB
REM =========================
echo Deploying MongoDB...
oc apply -f infrastructure/k8s/mongo-pvc.yaml
oc apply -f infrastructure/k8s/mongo-service.yaml
oc apply -f infrastructure/k8s/mongo-deployment.yaml
echo MongoDB deployment done.
echo.

REM =========================
REM 2. Build and push db-soldier Docker image
REM =========================
echo Building db-soldier Docker image...
docker build -t db-soldier .
docker tag db-soldier shuki120/db-soldier:latest
docker push shuki120/db-soldier:latest
echo Docker image pushed.
echo.

REM =========================
REM 3. Deploy db-soldier
REM =========================
echo Deploying db-soldier...
oc apply -f infrastructure/k8s/db-soldier-service.yaml
oc apply -f infrastructure/k8s/db-soldier-deployment.yaml
oc apply -f infrastructure/k8s/db-soldier-route.yaml
echo db-soldier deployment done.
echo.

REM =========================
REM 4. Get route and open FastAPI docs
REM =========================
echo Getting db-soldier route...
for /f "tokens=*" %%i in ('oc get route db-soldier -o jsonpath^="{.spec.host}"') do set FASTAPI_HOST=%%i
set FASTAPI_URL=http://%FASTAPI_HOST%/docs

echo FastAPI docs URL is: %FASTAPI_URL%
echo Opening FastAPI docs in browser...
start "" %FASTAPI_URL%
echo Done!
pause
