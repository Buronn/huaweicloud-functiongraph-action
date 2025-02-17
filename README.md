# Huawei FunctionGraph Deploy Action

The Huawei FunctionGraph Deploy Action is a GitHub Action that deploys functions to Huawei Cloud's FunctionGraph. It supports both ZIP code deployments and custom Docker image deployments using SWR, and provides options for VPC configuration, environment variable injection, and trigger creation.

> **Disclaimer:** This project is currently in version 0.1.0 and does not yet implement all functionalities available in Huawei Cloud's CLI (KooCli). Contributions are welcome to enhance and expand the project's features.

## Overview

This action performs the following tasks:

1. **Authentication:** Authenticates with Huawei Cloud using the provided access keys and region.
2. **CLI Setup:** Sets up the Huawei Cloud CLI (KooCli).
3. **Project Configuration:** Retrieves and sets the Huawei FunctionGraph Project ID.
4. **Argument Building:** Constructs command-line arguments for VPC settings, function code, environment variables, and custom image parameters.
5. **Docker Operations (if applicable):** Logs into the Docker repository and builds/pushes a Docker image when using a custom Docker image.
6. **Function Deployment:** Checks if the function exists, updating its code/configuration if it does or creating a new function if it does not.
7. **Trigger Management:** Creates or updates function triggers based on provided trigger configurations.

## Prerequisites

- A Huawei Cloud account with the necessary permissions.
- Valid Huawei Cloud **Access Key ID** and **Secret Access Key**.
- Appropriate configuration values for the region, VPC, custom image parameters, etc.
- GitHub Secrets and Variables configured for sensitive data and environment-specific values.

## Inputs

### Credentials

- **`access_key_id`** (required): Huawei Cloud Access Key ID.
- **`secret_access_key`** (required): Huawei Cloud Secret Access Key.

### Function Configuration

- **`region`** (required): Region where the function will be deployed (e.g., `la-south-2`).
- **`func_name`** (required): Name of the function to create.
- **`package`**: Function package (default: `"default"`).
- **`runtime`** (required): Function runtime (e.g., `Python3.10` or `Custom Image`).
- **`timeout`** (required): Maximum execution time (in seconds, range: 3-259200).
- **`handler`** (required): Function handler (e.g., `main.handler`).
- **`memory_size`** (required): Memory allocated to the function in MB (e.g., `256`).

### Code Settings

- **`code_path`**: Path to the folder containing the function code (relative to the repository).
- **`code_type`**: Function code type. Options: `inline`, `zip`, `obs`, `jar`, `Custom-Image-Swr` (default: `"zip"`).
- **`code_filename`**: Code file name (required if `code_type` is `zip`).
- **`code_link`**: URL for the function code.

### VPC Configuration

- **`func_vpc_domain_id`**: Domain name ID for the VPC.
- **`func_vpc_namespace`**: Project ID for the VPC.
- **`func_vpc_vpc_name`**: VPC name.
- **`func_vpc_vpc_id`**: VPC ID (required if VPC is configured).
- **`func_vpc_subnet_name`**: Subnet name.
- **`func_vpc_subnet_id`**: Subnet ID (required if VPC is configured).
- **`func_vpc_cidr`**: Subnet mask (CIDR).
- **`func_vpc_gateway`**: Gateway.
- **`func_vpc_security_groups`**: Security groups (comma-separated values).
- **`xrole`**: Huawei Cloud Agency name with permissions (required when configuring VPC).

### Custom Image (SWR) Settings

- **`dockerfile_path`**: Path to the Dockerfile for building the image (relative to the repository).
- **`custom_image_enabled`**: Enables the use of Custom Image (`true`/`false`, default: `"false"`).
- **`custom_image_image`**: Full image address. If left empty, it is generated using `custom_image_organization`, `custom_image_image_name`, and `custom_image_image_tag`.
- **`custom_image_image_tag`**: Image tag (default: `"latest"`).
- **`custom_image_organization`**: Organization to build the image.
- **`custom_image_image_name`**: Image name.
- **`custom_image_command`**: Command to start the container image.
- **`custom_image_args`**: Command-line parameters to start the image.
- **`custom_image_working_dir`**: Container working directory.
- **`custom_image_uid`**: User ID for the container.
- **`custom_image_gid`**: User group ID for the container.

### Trigger Settings

- **`trigger_enabled`**: Enables the creation of triggers for the function (`true`/`false`, default: `"false"`).
- **`trigger_configs`**: Trigger configuration in JSON array format. Each object must include at least the `trigger_type_code` parameter and may include additional parameters that will be added with the prefix `--event_data.` (default: `"[]"`).

### Environment Variables for Function Data

The action also processes environment variables prefixed with:

- **`FGE_`**: These are passed as encrypted environment variables.
- **`FG_`**: These are passed as user environment variables.

## Examples

### Example 1: Deploy Function Using ZIP Code with VPC and Python Runtime

```yaml
name: Deploy FunctionGraph

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      FGE_API_KEY: ${{ secrets.FGE_API_KEY }}
      FG_OTHER_VAR: "example-value"
      
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Deploy Function (ZIP Code, VPC, Python)
        uses: Buronn/huaweicloud-functiongraph-action@v0.1.0
        with:
          access_key_id: ${{ secrets.HW_ACCESS_KEY }}
          secret_access_key: ${{ secrets.HW_SECRET_KEY }}
          region: ${{ vars.HW_REGION }}
          func_name: "zip-function-vpc"
          package: "default"
          runtime: "Python3.10"
          timeout: 30
          handler: "index.handler"
          memory_size: 256
          code_path: "src/my-python-function"
          code_type: "zip"
          func_vpc_vpc_id: ${{ vars.HW_VPC_ID }}
          func_vpc_subnet_id: ${{ vars.HW_SUBNET_ID }}
          xrole: ${{ vars.HW_XROLE }}
```

### Example 2: Deploy Function Using a Custom Docker Image with VPC, Python Runtime, and a Cron Trigger

```yaml
name: Deploy FunctionGraph

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      FGE_API_KEY: ${{ secrets.FGE_API_KEY }}
      FG_OTHER_VAR: "example-value"
      
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Deploy Function (Custom Docker Image, VPC, Python) with Cron Trigger
        uses: Buronn/huaweicloud-functiongraph-action@v0.1.0
        with:
          access_key_id: ${{ secrets.HW_ACCESS_KEY }}
          secret_access_key: ${{ secrets.HW_SECRET_KEY }}
          region: ${{ vars.HW_REGION }}
          func_name: "custom-image-function-vpc"
          package: "default"
          runtime: "Custom Image"
          timeout: 30
          handler: "-"
          memory_size: 256
          xrole: ${{ vars.HW_XROLE }}

          code_path: "src/custom-image-function"  
          code_type: "Custom-Image-Swr"
          
          dockerfile_path: "Dockerfile"
          custom_image_enabled: "true"
          custom_image_image_name: "custom-function-image"
          custom_image_image_tag: "latest"
          custom_image_organization: "my-dev-team"

          func_vpc_vpc_id: ${{ vars.HW_VPC_ID }}
          func_vpc_subnet_id: ${{ vars.HW_SUBNET_ID }}

          trigger_enabled: "true"
          trigger_configs: '[{"trigger_type_code": "TIMER", "schedule_type": "Cron", "schedule": "0 */5 * * * *", "name": "EveryFiveMinutes"}]'
```

## Contributing

Contributions are welcome! If you'd like to contribute enhancements or bug fixes, please follow the repository guidelines and open a pull request.

## Issues

If you encounter any issues or have suggestions for improvements, please open an issue in the repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.