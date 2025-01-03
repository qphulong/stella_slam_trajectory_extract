# Building Stella SLAM Docker Images

Follow these steps to build the Stella SLAM Docker images:

## Step 1: Clone the Repository
Clone the Stella SLAM repository with all submodules:
```bash
git clone --recursive https://github.com/stella-cv/stella_vslam.git
cd stella_vslam
```

## Step 2: Build the Docker Image
Ensure you are using the correct Dockerfile name and command for the build.
Dockerfile.iridescense vs Dockerfile.iridescence

### Standard Build Command
Use the following command to build the Docker image:
```bash
docker build -t stella_vslam-iridescense -f Dockerfile.iridescense .
```

### Faster Build Command
For a faster build, utilize multiple threads:
```bash
# Build the Docker image using available CPU threads minus one
docker build -t stella_vslam-iridescense -f Dockerfile.iridescense . --build-arg NUM_THREADS=$(expr $(nproc) - 1)
