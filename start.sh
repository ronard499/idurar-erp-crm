#!/bin/bash

# Start the Django backend
cd django_backend
./start_server.sh > backend.log 2>&1 &
echo "Django backend started on port 12000"

# Wait for the backend to start
sleep 5

# Start the frontend
cd ../frontend
npm run dev -- --port 12001 --host 0.0.0.0 > frontend.log 2>&1 &
echo "Frontend started on port 12001"

echo "IDURAR ERP CRM is now running!"
echo "Backend: https://work-1-hoawaswwbhuszcua.prod-runtime.all-hands.dev/api/"
echo "Frontend: https://work-2-hoawaswwbhuszcua.prod-runtime.all-hands.dev/"
echo "Default admin user: admin@demo.com / admin123"