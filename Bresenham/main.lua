require "math"
local WIDTH = 900
local HEIGHT = 600


function round(x)
    return x>=0 and math.floor(x+0.5) or math.ceil(x-0.5)
  end

function naivedraw(x1, y1, x2, y2)
    
    love.graphics.print("NAIVE LINE DRAW ALGORITHM")
    love.graphics.print('( ' .. x1 ..  ', ' .. y1 .. ' )' , x1 - 15, y1 - 15)
    --
    m = (y2 - y1)/(x2 - x1) -- Calculate the slope m
    for x=x1 , x2, 1 do -- for every x from the beginning to the end
      y = round(m*x)  -- find the closest integer of the product slope * x
      love.graphics.points(x,y) -- draw the pixel
    --
    love.graphics.print('( ' .. x2 ..  ', ' .. y2 .. ' )' , x2, y2)
    end
    -- This algorithm is slow, because it requires floating point multiplication (m * x)
    -- and the computation of the round value of that result
    -- all of this in a loop
end

function bresenham(x1, y1, x2, y2)
    -- Bresenham was designed to get rid of floats
    -- Because float computation is expansive in terms of speed & memory
    -- It is optimal.
    love.graphics.print("BRESENHAM LINE DRAW ALGORITHM")
    love.graphics.print('( ' .. x1 ..  ', ' .. y1 .. ' )' , x1 - 15, y1 - 15)
    --
    x = x1
    y = y1
    dx = x2 - x1
    dy = y2 - y1
    dec = 2*dy - dx -- decision variable
    while (x <= x2) do
        love.graphics.points(x,y) -- Draw current pixel
        x = x + 1 -- Increment x
        if (dec < 0) then -- the pixel is closer to the current pixel
            dec = dec + 2 * dy 
        else              -- the pixel is farther than the current pixel
            dec = dec + (2*dy) - (2*dx) 
            y = y + 1 -- Increment y
        end
    end
    -- Bresenham works only with integers, so it is fast.
    love.graphics.print('( ' .. x2 ..  ', ' .. y2 .. ' )' , x2, y2)

end

function love.load()
    love.window.setMode(WIDTH, HEIGHT)
    
end

function love.update()
    
end


function love.draw()
    x1 = 50
    y1 = 50
    x2 = 768
    y2 = 325
    -- naivedraw(x1, y1, x2, y2)
    bresenham(x1, y1, x2, y2)

end

