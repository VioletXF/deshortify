# use ffmpeg to add black screen to the end of the video, to avoid YouTube's short video detection

import ffmpeg
import sys
import os
if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # measure the duration of the video
    probe = ffmpeg.probe(input_file)["streams"][0]
    ext = input_file.split(".")[-1]
    video_duration = float(probe["duration"])
    duration = 181 - video_duration
    if duration <= 0:
        print("Video is already 3 minutes or longer.")
        exit(0)
    width = int(probe["width"])
    height = int(probe["height"])
    r_frame_rate = probe["r_frame_rate"]
    frame_rate = float(r_frame_rate.split("/")[0]) / float(r_frame_rate.split("/")[1])

    # make a black screen video which matches the format of the input video, to fill 3 minutes.
    black_video = f"./{hash(input_file)}_black.{ext}"
    ffmpeg.input(f"color=c=black:s={width}x{height}:r={frame_rate}:d={duration}", f="lavfi").output(black_video).run()
    concat_file = f"./{hash(input_file)}_concat_list.txt"
    with open(concat_file, "w") as f:
        f.write(f"file '{input_file}'\n")
        f.write(f"file '{black_video}'\n")
    
    # concatenate the input video and the black screen video with audio
    ffmpeg.input(concat_file, format='concat', safe=0).output(output_file, c='copy').run()
    os.remove(concat_file)
    os.remove(black_video)




