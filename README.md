# Configuration

To configure your application data, replace '{}' variables accordingly in the file `samconfig.toml`

[Install AWS CLI](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html)

[Install SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

# Deployment

After configuring, you can deploy your application by running the following command in the directory of this project:

### Production:

`sam deploy -t .\uplandApi.yaml`

### Sandbox:

`sam deploy -t .\uplandApi.yaml --config-file samconfig-sandbox.toml`

## Deployment Outputs

The deployment generates three outputs, 
- Root url generated for your application
- GET code endpoint for new upland integration
- POST webhook endpoint needed to finish application setup in [upland dev portal](https://developer.upland.me/)

# Additional Steps

If you need to pair your application's User Id with Upland's, modify the file `getCode/app.py` and develop the logic for setting `userId` variable