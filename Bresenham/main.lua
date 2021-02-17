require "math"
local WIDTH = 900
local HEIGHT = 600


function round(x)
    return x>=0 and math.floor(x+0.5) or math.ceil(x-0.5)
  end

function naiveDraw(x1, y1, x2, y2)
    
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

function naiveBresenham(x1, y1, x2, y2)
    -- Bresenham was designed to get rid of floats
    -- Because float computation is expansive in terms of speed & memory
    -- It is optimal.
    love.graphics.print("NAIVE BRESENHAM LINE DRAW ALGORITHM (FIRST OCTANT)")
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
        if (dec < 0) then -- the pixel is closer to the actual point
            dec = dec + 2 * dy 
        else              -- the pixel is farther than the actual point
            dec = dec + (2*dy) - (2*dx) 
            y = y + 1 -- Increment y
        end
    end
    -- Bresenham works only with integers, so it is fast.
    -- However, the lines with origin in any other octant will not be draw correctly
    -- as this version of the algorithm doesn't address this issue yet.
    -- see Bresenham for a general case implementation.
    love.graphics.print('( ' .. x2 ..  ', ' .. y2 .. ' )' , x2, y2)

end

function positiveBresenham(x1, y1, x2, y2)
    -- Bresenham implementation for first and second octant.
    -- 
    love.graphics.print("BRESENHAM LINE DRAW ALGORITHM")
    love.graphics.print('( ' .. x1 ..  ', ' .. y1 .. ' )' , x1 - 15, y1 - 15)
    --
    x = x1
    y = y1
    dx = x2 - x1
    dy = y2 - y1
    dec = 0
    if dx > 0 and dy > 0 then -- first & second octant
        if dx < dy then -- second octant
            dec = dy - 2*dx -- decision variable
            while (y < y2) do
                love.graphics.points(x,y) -- Draw current pixel
                if dec < 0 then
                    dec = dec + 2 * dy
                    x = x + 1
                end
                dec = dec - 2 * dx 
                y = y + 1
            end
        else -- first octant
            dec = dx - 2*dy
            while (x < x2) do
                love.graphics.points(x,y) -- Draw current pixel
                if dec < 0 then -- Keep drawing pixels (no need to go up yet)
                    dec = dec + 2 * dx
                    y = y + 1
                end
                dec = dec - 2 * dy -- Go up
                x = x + 1
            end

        end
    end

    -- 
    love.graphics.print('( ' .. x2 ..  ', ' .. y2 .. ' )' , x2, y2)

end

function Bresenham(x1, y1, x2, y2)
    -- Bresenham implementation for all octants.
    --
    love.graphics.print("Bresenham implementation for all octants.")
    love.graphics.print('( ' .. x1 ..  ', ' .. y1 .. ' )' , x1 - 15, y1 - 15)
    --
    x = x1
    y = y1
    dx = x2 - x1
    dy = y2 - y1

    xend = 0
    yend = 0

    -- Make copies so positive deltas for easier iterations
    dx1 = math.abs(dx)
    dy1 = math.abs(dy)

    decX = 2*dy1 - dx1 -- decision variable for X axis
    decY = 2*dx1 - dy1 -- decision variable for Y axis

    if (dy1 < dx1) then -- The line is most likely horizontal
        -- if the slope is positive
        -- draw it from left to right
        if (dx >= 0) then
            x = x1
            y = y1
            xend = x2
        -- else draw it from right to left
        else 
            x = x2
            y = y2
            xend = x1
        end
        love.graphics.points(x,y) -- Draw first pixel
        -- Rasterize the line
        for i=0, xend, 1 do
            x = x + 1 -- increment x
            -- now depending on which octant we are
            if decX < 0 then
                decX = decX + 2 * dy1
            else
                if ( (dx < 0 and dy < 0) or (dx > 0 and dy > 0) ) then
                    y = y + 1
                else
                    y = y - 1
                end
                decX = decX + 2 * (dy1 - dx1)
            end
            -- Draw the pixel but in the rasterized position
            love.graphics.points(x,y)
        end
    else -- The line is most likely vertical
         -- Follow the same logic, but for y instead of x
         -- Draw the line bottom to top
        if (dy >= 0) then
            x = x1
            y = y1
            yend = y2
        -- else draw it from top to bottom
        else 
            x = x2
            y = y2
            yend = y1
        end
        love.graphics.points(x,y) -- Draw first pixel
        -- Rasterize the line
        for j=0, yend, 1 do
            y = y + 1 -- increment x
            -- now depending on which octant we are
            if decY < 0 then
                decY = decY + 2 * dx1
            else
                if ( (dx < 0 and dy < 0) or (dx > 0 and dy > 0) ) then
                    x = x + 1
                else
                    x = x - 1
                end
                decY = decY + 2 * (dx1 - dy1)
            end
            -- Draw the pixel but in the rasterized position
            love.graphics.points(x,y)
        end
    end
    -- 
    love.graphics.print('( ' .. x2 ..  ', ' .. y2 .. ' )' , x2, y2)

end

function love.load()
    love.window.setMode(WIDTH, HEIGHT)
    
end

function love.update()
    
end


function love.draw()
    x1 = 456
    y1 = 599
    x2 = 23
    y2 = 18
    -- naiveDraw(x1, y1, x2, y2)
    -- naiveBresenham(x1, y1, x2, y2)
    -- positiveBresenham(x1, y1, x2, y2)
    Bresenham(x1, y1, x2, y2)


end

