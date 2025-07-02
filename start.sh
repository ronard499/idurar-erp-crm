#!/bin/bash

# Start Django backend
cd django_backend
python manage.py runserver 0.0.0.0:12010 > backend.log 2>&1 &
echo "Django backend started on port 12010"

# Wait for the backend to start
sleep 5

# Start frontend
cd ../frontend
npm run dev -- --port 12014 --host 0.0.0.0 > frontend.log 2>&1 &
echo "Frontend started on port 12014"

echo "IDURAR ERP CRM is now running!"
echo "Backend: https://work-1-hoawaswwbhuszcua.prod-runtime.all-hands.dev:12010/api/"
echo "Frontend: https://work-2-hoawaswwbhuszcua.prod-runtime.all-hands.dev:12014/"
echo "Default admin user: admin@example.com / admin123"