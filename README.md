# Python PyPI Package Template

A minimal template for creating Python packages with a simple "Hello World" example.

## Quick Start

### 1. Use this template

Click the "Use this template" button on GitHub to create your own repository:

### 2. Install dependencies

```bash
# Run the development setup script
.\tasks\dev_sync.ps1
```

### 3. Customize the package

#### Rename the package

1. Rename directories:
   ```bash
   mv src/whitelabel src/YOUR_PACKAGE_NAME
   mv tests/whitelabel tests/YOUR_PACKAGE_NAME
   ```

2. Update `pyproject.toml`:
   - Change `name = "whitelabel"` to `name = "YOUR_PACKAGE_NAME"`
   - Update author information
   - Update repository URLs

3. Update import statements in your code from `whitelabel` to `YOUR_PACKAGE_NAME`


## Next Steps

1. Replace the hello_world function with your own code
2. Add your functions to `src/YOUR_PACKAGE_NAME/functions/`
3. Write tests in `tests/YOUR_PACKAGE_NAME/`
4. Update `pyproject.toml` with your package details

## CI/CD Configuration

### SonarQube Setup

To enable SonarQube analysis in your CI/CD pipeline, set the following variables:

- `SONAR_TOKEN`: Set as a **secret** in your CI/CD platform (authentication token for SonarQube)
- `SONAR_PROJECT_KEY`: Set as an **environment variable** in your CI/CD pipeline (unique key for your project, e.g., `your-org_your-repo`)

`SONAR_HOST_URL` is typically configured at the organization level.

## License

MIT License
