from ultralytics import YOLO
import torch

# if torch.cuda.is_available():
#     device = torch.cuda.current_device()
#     print(f"Current GPU device: {torch.cuda.get_device_name(device)}")
#     print(f"Total memory: {torch.cuda.get_device_properties(device).total_memory / (1024**3)} GB")
# else:
#     print("GPU is not available.")
#
# # Kiểm tra số lượng GPU
# num_gpus = torch.cuda.device_count()
#
# if num_gpus > 0:
#     print("Có", num_gpus, "GPU có sẵn trong máy tính.")
#     for i in range(num_gpus):
#         gpu_name = torch.cuda.get_device_name(i)
#         print("GPU", i, ":", gpu_name)
# else:
#     print("Không tìm thấy GPU trong máy tính.")
# # Load a model
# model = YOLO("yolov8m.yaml")  # build a new model from scratch
# model = YOLO("best.pt")  # load a pretrained model (recommended for training)

if __name__ == '__main__':
    # model.train(data=r"C:\Users\Admin\PycharmProjects\Fire protection system\Data\data.yaml", epochs=80, device='0') # train the model with GPU(0)
    model = YOLO("best.pt")
    metrics = model.val() # evaluate model performance on the validation set
    # model = YOLO(r"C:\Downloads\Train\runs\detect\train\weights\last.pt")  # continue training
    # model.train(resume=True)


# ffmpeg -i "Video/Spark2.mp4" -c:v copy -an Spark2.mp4