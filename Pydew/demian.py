for a in range(-chunksy,chunksy+1):
    for b in range(-chunksx,chunksx+1):
        y = index2[0]+a
        x = index2[1]+b
        if y > -1 and x > -1 and x < xl and y < yl:
            exec(f"SCREEN.blit(Tile{str(WallsShape[y][x])}, ({x}*size-CamX+WIDTH/2,{y}*size-CamY+HEIGHT/2))")