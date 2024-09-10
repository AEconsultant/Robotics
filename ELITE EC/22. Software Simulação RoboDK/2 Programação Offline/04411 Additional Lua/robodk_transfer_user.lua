sleep(0.3)

function Transf_to_base(userno,ttl_count)
    local user = get_user_frame(1)
    for i=0,ttl_count,1  do
        local v_tmp = {get_global_variable('V'..i)}
        local v_inbase = pose_mul(user,v_tmp)
        set_global_variable('V'..i,v_inbase[1],v_inbase[2],v_inbase[3],v_inbase[4],v_inbase[5],v_inbase[6])
    end
end

while true do
    B000 =get_global_variable('B000')
    if(B000 ==1)  then
        B010 =get_global_variable('B010')
        Transf_to_base(1,B010)
        set_global_variable('B000',0)
    end
    sleep(0.1)
end
