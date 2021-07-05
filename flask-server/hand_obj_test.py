from model.faster_rcnn.resnet import resnet

fasterRCNN = resnet(pascal_classes, 101, pretrained=False, class_agnostic=args.class_agnostic)