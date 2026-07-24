from transformers import (
    DetrImageProcessor,
    TableTransformerForObjectDetection
)
from PIL import Image
import torch


class TableDetector:

    def __init__(self):
        #Loads image preprocessing pipeline
        #using pre-trained Table Transformer (TATR) model from_pretrained() downloads (the first time) and loads a model that has already been trained by someone else.
        self.processor = (DetrImageProcessor.from_pretrained("microsoft/table-transformer-detection"))
        #Loads the actual AI model
        self.model = (TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection"))

    def detect(self, image):
        #Converts OpenCV/Numpy image into PIL image
        pil_img = Image.fromarray(image)
        
        #Resize the image
        #create pytorch tensor
        #inputs={"pixel_values": tensor(...)}
        inputs = self.processor(images=pil_img,return_tensors="pt")
        
        #The ** operator unpacks the dictionary into keyword arguments.
        #unpacks the directory
        outputs = self.model(**inputs) 
        
        
        #[-1] will convert img size in reverse like height, width
        """ 
        results contains 
        {
            "scores": tensor([0.98, 0.87]),
            "labels": tensor([0, 0]),
            "boxes": tensor([
                [100, 250, 900, 1400],
                [950, 300, 1500, 1200]
            ])
        }
        """
        results = (self.processor.post_process_object_detection(outputs,threshold=0.6,target_sizes=torch.tensor([pil_img.size[::-1]]))[0])

        tables = []

        for box in results["boxes"]:
            #convert Torch Tensor to list 
            tables.append(box.tolist())

        return tables
    
    
    """
    it returns
    [
    [100.5, 200.2, 900.8, 1400.4],
    [950.1, 300.6, 1500.3, 1200.7]
    ]
    """