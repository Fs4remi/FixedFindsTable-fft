import React from 'react'

const validTime = (props) => {
    let userTime = ""

    if (parseInt(props.Time) < 7 || parseInt(props.Time) > 21) {
        userTime = "Invalid Class Start Time"
    }

    const style = {
        color: 'red',
        fontSize: '15px'
    }
    
    return(
        <div>
            <p style={style}>{userTime}</p>
        </div>
    )

} 

export default validTime