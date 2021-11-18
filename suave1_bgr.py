# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 13:31:39 2021

@author: hbuzzi
"""
import cv2
import sys
import numpy as np
from scipy import signal


def get_rect_zone(Imagem):
    ###Nested Function
    def mouse_event(event, col, lin, flags, *userdata): #Função clique mouse
        if event == cv2.EVENT_LBUTTONDOWN: #Se pressionar o botão esquerdo
            # global rect_point
            #Cria variáveis globais da col/lin da ref desejada
            rect_point.append((col,lin))
            copied = Imagem.copy() #Cria uma cópia
            cv2.circle(copied, (col, lin), 1,(0,0,255),-1) #Desenha círculo no ponto clicado
            cv2.imshow(w_name,copied) #Mostra o círculo na imagem copiada (não modifica o frame original), para o usuário saber se está certo
        if event == cv2.EVENT_LBUTTONUP:
            rect_point.append((col,lin))
            copied = Imagem.copy() #Cria uma cópia
            cv2.rectangle(copied, rect_point[0], rect_point[1],(0,0,255), 1)
            cv2.imshow(w_name,copied)

######### Começa função
    w_name = "Selecione o fundo de referencia" #Nome da janela
    cv2.imshow(w_name, Imagem) #Mostra o frame
    while True: #Loop para cada frame
        
        key = cv2.waitKey(0) #Espera um input do teclado do usuário
        if key == 27: #Se pressionou esc
            cv2.destroyWindow(w_name) #Fecha a janela
            sys.exit() #Termina o código
        elif key == ord('C') or key == ord('c'):
            rect_point = []
            cv2.setMouseCallback(w_name, mouse_event) # Chama função de clicar mouse
            key = cv2.waitKey(0) # Espera o usuário pressionar
            if key == 13: #Se deu Enter
                Blur_zone = I[rect_point[0][1]:rect_point[1][1],rect_point[0][0]:rect_point[1][0]]
                cv2.setMouseCallback(w_name, lambda *args : None) #Termina a função do mouse
                break #Sai do loop
            elif key == 32: #Se deu espaço
                cv2.setMouseCallback(w_name, lambda *args : None) #Termina a função do mouse
                cv2.imshow(w_name, Imagem)
                continue #Vai pro próximo passo pois ele vai selecionar outro valor ou sair
    cv2.destroyWindow(w_name) #Fecha a janela
    return Blur_zone,rect_point#Retorna a referência

def convolve_interest_region(Zone, kernel, Limiar): # Recebe a região a ser filtrada, o kernel, o limiar (dita onde aplicar)
    centro = kernel.shape[0]//2 # pega o centro do kernel (importante para saber a janela)
    h, w, ch = Zone.shape #pega o tamanho da região, para poder iterar sobre
    mask = Zone.copy() #cria a máscara a partir da cópia da região, isso acelera o trabalho
    for i in range(centro,h-centro): #Tem que ter essa distância inicial do centro, e um final decrescido o centro, para evitar que a janela de convolução atinja
    # pixels fora da imagem, resultando em erro
        for j in range(centro,w-centro):
            if (Zone[i,j,:]>Limiar).all(): #Se o Pixel for muito claro
                continue #Não precisa realizar nada, o pixel já está copiado na máscara
            else: #Se for muito escuro
                mask[i,j,:] = cv2.filter2D(src = Zone[i-centro:i+centro,j-centro:j+centro,:], ddepth = -1, kernel = kernel)[centro,centro,:] #Aplica a convolução para filtrar
                #Pega apenas o pixel do centro pois é ele que desejamos filtrar
    return mask #Retorna a máscara

def neighbor_blur_kernel(sigma):
    size = 6*sigma+1
    neighBlurKernel = np.ones(shape = (size,size), dtype = np.float64())/((size**2)-1) #Cria Kernel equilibrado em todos os pixels
    neighBlurKernel[size//2,size//2] = 0 #Ignora o pixel do centro
    return neighBlurKernel

def Inverted_gauss_kernel(sigma):
    size = 6*sigma+1
    kernel_gauss_inv = (cv2.getGaussianKernel(ksize = size, sigma = sigma))**-1 #Gera o filtro Gaussiano pela função pronta do CV2 e inverte
    # ksize - kernel size, should be odd and positive (3,5,...)
    # sigma - Gaussian standard deviation. If it is non-positive, it is computed from ksize as sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8 
    # ktype - Type of filter coefficients (Optional)
    kernel_gauss_inv = kernel_gauss_inv/kernel_gauss_inv.sum() #Equilibra os valores do kernel
    kernel_gauss_inv = signal.convolve(kernel_gauss_inv,kernel_gauss_inv.transpose()) #Cria a matriz a partir da convolução do kernel em si mesmo (propriedade linear da convolução)
    return kernel_gauss_inv

def imshow_close_withEsc(image,text): #Função que mostra a imagem e permite fechá-la com qualquer tecla
    cv2.imshow(text, image) #Mostra imagem
    key = cv2.waitKey(0) #Espera tecla
    if key != None:  #Se tiver alguma tecla
        cv2.destroyWindow(text) #Fecha a imagem
        return
        
    
###### CODE START ######################
######## User defined parameters
I = cv2.imread('Tatoo1.jpg')  #Lê a imagem
Limiar = 150 #Limiar definido pelo usuário, utilizado como referência para captar o que é pra ser considerado como preto
sigma = 3

############ Região de trabalho
Blur_zone, rect_points = get_rect_zone(I) #Chama a função para definir a área de trabalho

################ Get kernels
Blur_Kernel = neighbor_blur_kernel(sigma) #Chama função do Kernel de vizinhança
kernel_inv_matrix = Inverted_gauss_kernel(sigma) #Chama função do Kernel inverso

################ Aplying masks
mask = convolve_interest_region(Blur_zone,kernel_inv_matrix, Limiar) #Aplica convolução com o Kernel sobre a região
imshow_close_withEsc(mask, "Primeira iteração")

mask = convolve_interest_region(mask,kernel_inv_matrix, Limiar) #Aplica convolução com o Kernel sobre a região
imshow_close_withEsc(mask, "Segunda iteração")

mask = convolve_interest_region(mask,Blur_Kernel, Limiar) #Aplica convolução com o Kernel sobre a região
imshow_close_withEsc(mask, "Aplicação do Blur")

I[rect_points[0][1]:rect_points[1][1],rect_points[0][0]:rect_points[1][0]] = mask #Coloca a máscara filtrada sobre a região da imagem original
imshow_close_withEsc(I, "Resultado")






