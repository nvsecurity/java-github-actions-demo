echo "nightvision swagger extract ./ -t javaspringvulny-api --lang spring"
nightvision swagger extract ./ -t javaspringvulny-api --lang spring
echo "==================================================================="
read
echo "nightvision swagger diff openapi.yaml openapi-spec.yml "
nightvision swagger diff openapi.yaml openapi-spec.yml 
