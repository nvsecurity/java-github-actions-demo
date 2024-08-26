echo "nightvision swagger extract ./ -t javaspringvulny-api --lang spring"
nightvision swagger extract ./ -t javaspringvulny-api --lang spring
echo "==================================================================="
read
echo "nightvision swagger diff -n openapi-spec.yml -o openapi.yaml"
nightvision swagger diff -n openapi-spec.yml -o openapi.yaml 
