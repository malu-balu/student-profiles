# Replace YOUR_PUBLIC_IP with your EC2 Public IPv4 address.
# Local testing uses localhost. EC2 testing uses http://YOUR_PUBLIC_IP:5000

# Health check
curl -i http://localhost:5000/api/health
curl -i http://YOUR_PUBLIC_IP:5000/api/health

# API info
curl -i http://localhost:5000/api/info

# READ all
curl -i http://localhost:5000/api/students

# READ one
curl -i http://localhost:5000/api/students/1

# CREATE success
curl -i -X POST http://localhost:5000/api/students \
  -H 'Content-Type: application/json' \
  -d '{"name":"Zara","grade":"A","course":"DevOps","city":"Topi"}'

# CREATE error: invalid grade
curl -i -X POST http://localhost:5000/api/students \
  -H 'Content-Type: application/json' \
  -d '{"name":"Bad Grade Student","grade":"Z"}'

# UPDATE with PUT
curl -i -X PUT http://localhost:5000/api/students/1 \
  -H 'Content-Type: application/json' \
  -d '{"grade":"A","city":"Peshawar"}'

# PARTIAL UPDATE with PATCH
curl -i -X PATCH http://localhost:5000/api/students/1 \
  -H 'Content-Type: application/json' \
  -d '{"course":"Cloud Computing"}'

# DELETE
curl -i -X DELETE http://localhost:5000/api/students/2

# Count
curl -i http://localhost:5000/api/students/count

# Search
curl -i 'http://localhost:5000/api/students/search?grade=A'
curl -i 'http://localhost:5000/api/students/search?name=Ali'

# Stats and system
curl -i http://localhost:5000/api/stats
curl -i http://localhost:5000/api/system

# Error case: not found
curl -i http://localhost:5000/api/students/999
