curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDogu07v-gFGs5F83bTm-nf8SOnQA6E2BQ" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "said hi"}]
    }]
   }'