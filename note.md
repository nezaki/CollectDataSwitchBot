## 開発中のメモ

AWS CLI実行の準備（認証情報の取得と設定）
```
AWS_ACCOUNT_ID=
AWS_IAM_USER_NAME=n
AWS_IAM_ROLE_NAME=
AWS_ROLE_SESSION_NAME=

echo -n "mfa token: "
read MFA_TOKEN
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=

CREDENTIALS=$(aws sts assume-role \
  --serial-number arn:aws:iam::${AWS_ACCOUNT_ID}:mfa/mfa \
  --role-arn arn:aws:iam::${AWS_ACCOUNT_ID}:role/${AWS_IAM_ROLE_NAME} \
  --role-session-name ${AWS_ROLE_SESSION_NAME} \
  --duration-seconds 43200 \
  --token-code ${MFA_TOKEN} \
  --profile ${AWS_IAM_USER_NAME})

echo ${CREDENTIALS}

export AWS_ACCESS_KEY_ID=$(echo ${CREDENTIALS} | jq -r .Credentials.AccessKeyId)
export AWS_SECRET_ACCESS_KEY=$(echo ${CREDENTIALS} | jq -r .Credentials.SecretAccessKey)
export AWS_SESSION_TOKEN=$(echo ${CREDENTIALS} | jq -r .Credentials.SessionToken)
export AWS_DEFAULT_REGION=ap-northeast-1

echo \\nExpiration $(echo ${CREDENTIALS} | jq -r .Credentials.Expiration)
echo export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
echo export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
echo export AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
echo export AWS_DEFAULT_REGION=ap-northeast-1
echo export AWS_PROFILE=${AWS_IAM_USER_NAME}
```

ローカル(localstack)のDynamoDBにテーブル作成
```
aws --endpoint-url=http://localhost:4566 dynamodb create-table \
    --table-name device_status  \
    --attribute-definitions \
        AttributeName=DeviceID,AttributeType=S \
        AttributeName=Time,AttributeType=S \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --key-schema AttributeName=DeviceID,KeyType=HASH AttributeName=Time,KeyType=RANGE \
    --billing-mode PROVISIONED \
    --table-class STANDARD \
    --profile localstack

aws --endpoint-url=http://localhost:4566 dynamodb create-table \
    --table-name weather  \
    --attribute-definitions \
        AttributeName=CityID,AttributeType=S \
        AttributeName=Time,AttributeType=S \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --key-schema AttributeName=CityID,KeyType=HASH AttributeName=Time,KeyType=RANGE \
    --billing-mode PROVISIONED \
    --table-class STANDARD \
    --profile localstack
```

ローカル(localstack)のSecretManagerにシークレット作成
```
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret \
    --name SwitchbotApiToken \
    --secret-string "" \
    --profile localstack
    
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret \
    --name SwitchbotApiSecret \
    --secret-string "" \
    --profile localstack
    
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret \
    --name SwitchbotDeviceID \
    --secret-string "" \
    --profile localstack
```
```
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret \
    --name CurrentWeatherAppid \
    --secret-string "" \
    --profile localstack
```

メモ
```
docker compose up -d
```
```
docker compose down
```

```
pip freeze > app/requirements.txt

sam build

sam deploy \
  --config-file samconfig.toml \
  --parameter-overrides SwitchbotApiToken="" SwitchbotApiSecret="" SwitchbotDeviceID="" CurrentWeatherAppid=""
```
