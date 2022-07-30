from torchvision import models
from torchinfo import summary

if __name__ == '__main__':
    print("aaa")
    model = models.resnet18()
    summary(model)