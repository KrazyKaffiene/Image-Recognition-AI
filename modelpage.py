from common import *

directory_path = os.path.dirname(__file__) # file path of the file that the program is stored in

# Construct the model path
path = directory_path
path = os.path.join(path, "model.pth")

def unpickle(file_path):
    with open(file_path, 'rb') as file: # Open the file as a read bytes file
        foo = pickle.load(file, encoding = 'bytes')
    return foo

# Load up the model
model = (torch.load(path))
model.eval()

meta = unpickle(os.path.join(directory_path, 'meta'))
label_names = meta[b'fine_label_names']
label_names = [label.decode() for label in label_names]

def run(img, gradcam):
    img = np.array(img)
    img = cv2.resize(img, (32,32))
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img, 1)
    # Colour, width, height
    img = img.transpose(2,0,1)
    img = img[np.newaxis, :, :, :]
    img *= 255
    img = 255 - img
    image = torch.tensor(img, dtype= torch.float32, requires_grad=True)
    
    length = 16
    layer = length - int(gradcam * length)
    
    conv_model = model[:layer] # Convolutional block
    conv_output = conv_model(image)
    h = conv_output.retain_grad() # Store the gradients
    output = model[layer:](conv_output)
    
    # Get the back-propogation logit
    output_value = torch.max(output)
    output_value.backward()
    
    # Get the gradient
    grad = conv_output.grad
    grad = torch.mean(grad, dim=1)
    grad = grad.squeeze(0)
    conv_output = torch.mean(conv_output.detach(), dim=1).squeeze(0)
    c = conv_output * grad # Weight the activations
    threshold = torch.tensor([c.mean()-c.std()*1.2])
    d = c
    c[c < threshold] = torch.tensor(0)
    a = c
    c = cv2.resize(np.array(c),(32,32))
    c /= c.max()
    c = np.uint8(255 * c)
    c = cv2.applyColorMap(c, cv2.COLORMAP_JET)
    
    output = torch.squeeze(output)
    probabilities = torch.nn.functional.softmax(output, dim=0)
    probabilities = np.array(probabilities.detach())
    
    return probabilities, np.array(label_names), c

