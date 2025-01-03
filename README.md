# Building Stella SLAM Docker Images

Follow these steps to build the Stella SLAM Docker images:

## Step 1: Clone the Repository
Clone the Stella SLAM repository with all submodules:
```bash
git clone --recursive https://github.com/stella-cv/stella_vslam.git
cd stella_vslam
```

## Step 2: Build the Docker Image
Ensure you are using the correct Dockerfile name and command for the build. Note the difference between `Dockerfile.iridescense` and `Dockerfile.iridescence`.

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
```

## How to Run
1. Create an `input` directory:
   ```bash
   mkdir input
   ```
2. Place your VR360 video into the `input` directory.
3. Run the cells in the provided Jupyter Notebook (`.ipynb`) sequentially.
4. The output will be saved in the `output` directory.
