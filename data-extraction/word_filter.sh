state_words=(force cooperation welfare military tie economy gdp tension trade)

state_v_words=(increase decrease enhance safeguard maintain "continue" "expand" extend grow reduce surpass boost improve surge worsen escalate de-escalate protect weaken remain)

for file in `ls $1`; do
    for word in ${state_words[@]}; do
        full_path=$1"/"$file
        is_found=false
        if grep -q "\t$word" $full_path; then
            for v_word in ${state_v_words[@]}; do
                if grep -q "\t$v_word" $full_path; then
                    echo $full_path
                    is_found=true
                    break
                fi
            done
            if [ "$is_found" == true ]; then
                break
            fi
        fi
    done
done
