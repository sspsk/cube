import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def get_proj_coords(x,y,z):
    return x/np.abs(z),y/np.abs(z)

def rotate3d(x,y,z,theta):
    rx = x.mean()
    rz = z.mean()
    
    x = x - rx
    z = z - rz
    
    newx = np.cos(theta)*x - np.sin(theta)*z + rx
    newz = np.sin(theta)*x + np.cos(theta)*z + rz
    newy = y
    
    return newx,newy,newz

def render(X,Y,Z):
    
    proj_x,proj_y = get_proj_coords(X,Y,Z)
    
    x_max = 2
    y_max = 2
    
    scaled_x = proj_x/x_max
    scaled_y = proj_y/y_max
    
    
    x_width = 512
    y_width = 512


    pixel_x = scaled_x*x_width
    pixel_y = scaled_y*y_width

    pixel_x = x_width//2 + pixel_x
    pixel_y = y_width//2 + pixel_y
    
    pixel_x = pixel_x.round().astype(int)
    pixel_y = pixel_y.round().astype(int)
    
    img = np.zeros((x_width,y_width))

    for x,y in zip(pixel_x,pixel_y):
        img[y-2:y+3,x-2:x+3] = 1
          
    return img

if __name__ == "__main__":
    
    drag=False
    startX = None
    angle = 0
    cangle = None
    

    X = np.array([-1,1,1,-1,-1,1,1,-1])
    Y = np.array([1,1,-1,-1,1,1,-1,-1])
    Z = np.array([-5,-5,-5,-5,-7,-7,-7,-7])


    fig,ax = plt.subplots()
    im = ax.imshow(render(X,Y,Z))


    def on_move(event):
        global cangle
        if drag:
            delta = event.xdata - startX
            cangle = (delta/512)*2*np.pi + angle
            newX,newY,newZ = rotate3d(X,Y,Z,-cangle)
            im.set_data(render(newX,newY,newZ))
            event.canvas.draw()
            print(newX,newY,newZ,sep="\n")
            print(cangle)
            
            

    def enable_drag(event):
        global drag
        global startX
        drag=True
        if startX is None:
            startX = event.xdata
        
    def disable_drag(event):
        global drag
        global startX
        global angle
        drag=False
        startX = None
        angle = cangle

    def close(event):
        if event.key == 'q':
            plt.close(event.canvas.figure)

    
    cid = fig.canvas.mpl_connect("key_press_event", close)
    cid = fig.canvas.mpl_connect("button_press_event",enable_drag)
    cid = fig.canvas.mpl_connect("button_release_event",disable_drag)
    cid = fig.canvas.mpl_connect('motion_notify_event', on_move)

    plt.show()