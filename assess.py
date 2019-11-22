import argparse
from qrhandler import QRPictureHandler, QRVideoHandler
from yuvreader import YUVReader
from video_assessment import VideoQualityAssessment
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json

def ParseParameters(parameter_file):
  with open(parameter_file) as json_file:
    paras = json.load(json_file)
    return paras

def ExpandList(input):
  output = []
  for idx,value in enumerate(input):
    tmp = [idx for i in range(value)]
    output.extend(tmp)
  return output


if __name__ == "__main__":
  parse = argparse.ArgumentParser(description = 'manual to this script')
  parse.add_argument('--input', type=str, default="", help="Json file include input parameters.")
  argv = parse.parse_args()

  parameters = ParseParameters(argv.input)

  fig = plt.figure()
  ax1 = fig.add_subplot(211)
  ax2 = fig.add_subplot(212)

  raw_videos = parameters['raw_videos']
  test_videos = parameters['test_videos']
  framerate = int(parameters['framerate'])
  dimension = parameters['dimension']
  colorformat = parameters['color_format']
  duration = int(parameters['duration'])
  titles = parameters['titles']

  results = []
  for index, raw_video in enumerate(raw_videos):
    test_video = test_videos[index]
    assessment1 = VideoQualityAssessment(raw_video, test_video, (1280,720), "I420")
    found_ids1, psnr_data1, dropped_ids1 = assessment1.PSNRAssessment()
    framerate1 = assessment1.FrameRateAssessment(framerate, found_ids1, dropped_ids1)
    framerate1 = ExpandList(framerate1)
    results.append((found_ids1, psnr_data1, framerate1))

  labels =titles 
  p=None
  for index, result in enumerate(results):
    found_ids1, psnr_data1, framerate1 = result
    p = ax1.plot(found_ids1, psnr_data1, label=labels[index])
    ax1.axhline(sum(psnr_data1)/len(psnr_data1), color=p[0].get_color(), linestyle='dashed', linewidth=1)
    ax2.hist(framerate1, duration, histtype='step', align='mid')
  ax1.legend()
  ax2.xaxis.set_major_locator(ticker.MultipleLocator(1))

  plt.show()
