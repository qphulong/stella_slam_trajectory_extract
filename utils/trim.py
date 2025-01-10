import argparse
from moviepy import VideoFileClip

def time_to_seconds(time_str):
    """Convert a time string in MM:SS format to total seconds."""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def trim_video(input_file, output_file, start_time, end_time):
    # Load the video file
    video = VideoFileClip(input_file)
    
    # Trim the video from start_time to end_time
    trimmed_video = video.subclip(start_time, end_time)
    
    # Write the trimmed video to the output file
    trimmed_video.write_videofile(output_file, codec="libx264")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Trim a video file.")
    parser.add_argument("input_file", help="Path to the input video file.")
    parser.add_argument("output_file", help="Path to save the trimmed video.")
    parser.add_argument("start_time", help="Start time in MM:SS format.")
    parser.add_argument("end_time", help="End time in MM:SS format.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Convert the time strings to total seconds
    start_seconds = time_to_seconds(args.start_time)
    end_seconds = time_to_seconds(args.end_time)
    
    # Call the trim_video function with parsed arguments
    trim_video(args.input_file, args.output_file, start_seconds, end_seconds)

if __name__ == "__main__":
    main()

# Example usage
# python3 trim.py kyoto.mp4 output_video.mp4 3:10 4:39