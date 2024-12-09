import pygame
import pygame.camera
import numpy as np
import torch
import os
import cv2
import time
import matplotlib.pyplot as plt
import pickle

pygame.init()
pygame.camera.init()

from ui import *
    
UI = interface((1000,1000))
