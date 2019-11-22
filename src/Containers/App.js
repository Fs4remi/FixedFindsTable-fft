import React, {Component} from 'react';
import ValidTime from '../Components/ValidTime.js'
import './App.css';
import {Dropdown} from 'reactjs-dropdown-component';


class App extends Component {
  state = ({
    Day: [
      {
        id: 0,
        title: 'M',
        selected: false,
        key: 'Day',
      },
      {
        id: 1,
        title: 'Tu',
        selected: false,
        key: 'Day',
      },
      {
        id: 2,
        title: 'W',
        selected: false,
        key: 'Day',
      },
      {
        id: 3,
        title: 'Th',
        selected: false,
        key: 'Day',
      },
      {
        id: 4,
        title: 'F',
        selected: false,
        key: 'Day',
      },
      {
        id: 5,
        title: 'MW',
        selected: false,
        key: 'Day',
      },
      {
        id: 6,
        title: 'MWF',
        selected: false,
        key: 'Day',
      },
      {
        id: 7,
        title: 'MF',
        selected: false,
        key: 'Day',
      },
      {
        id: 8,
        title: 'WF',
        selected: false,
        key: 'Day',
      },
      {
        id: 9,
        title: 'TuTh',
        selected: false,
        key: 'Day',
      },
      {
        id: 10,
        title: 'FS',
        selected: false,
        key: 'Day',
      }
    ],
   
    userTime: "05:00",
    userClassMeetingDays: "NONE",
    submitableD: false,
    submitableT: false

  })

userTimeHandler = (event) => {
    this.setState({
      userTime: event.target.value
    })
    this.validTimeHandler()
    console.log("2.updateSubmitableDay TIME: ", this.state.userTime)
    console.log("3.supdateSubmitableDay submitableT: ", this.state.submitableT)
}

updateSubmitableDay = (id) => {
  this.setState({
    userClassMeetingDays: this.state.Day[id].title,
    submitableD : true
  })
  console.log("DAY", this.state.Day[id].title)
  console.log("selected", this.state.Day[id].selected)
  
}

/* Validates the time to be in 7-21 hr range AND updates the submitableT */
validTimeHandler = () => {
  //var submit = {this.state.submitableT}
  if (parseInt(this.state.userTime) < 7 || parseInt(this.state.userTime) > 21) {
      if (this.state.submitableT)  {
        this.setState({
          submitableT: false
        })
      }  
  }
  else{
    if(this.state.submitableT === false){
      this.setState({
        submitableT: true
      })
    }
  }
  console.log("1.in the validTimeHandler", this.state.submitableT)
  }

  /*Anthony's code 
  updateSubmitState = (id) => {
    let count = 0
    if (this.state.Day.id.selected) { count++}
    else {
      count--
    }
    //console.log("Count: ", count)
    if (count > 0 && count < 4) {
      console.log("here")
      this.setState({
        submitable: true
      })
    }
  }*/

  //Dropdown
  resetThenSet = (id, key) => {
    let temp = JSON.parse(JSON.stringify(this.state[key]));
    temp.forEach(item => item.selected = false);
    temp[id].selected = true;
    this.setState({
      [key]: temp
    });
    this.updateSubmitableDay(id)
  }

  render () {
    const console = () => {
      console.log("Current State: ", this.state.submitableT)
    }
    return (
      <div className='App'>
        <div className='InputBox'></div>
        <div className='header'>
        <h1>EBFF19</h1>
        <h2>Made Easy</h2>
        </div>
  
        <div className='dropDown'>
          {//dropdown set up
         } 
        
        <Dropdown
        titleHelper="Day"
        title="Class Days"
        list={this.state.Day}
        resetThenSet={this.resetThenSet}
        />
        </div>
        {//Mental Health and Psychiatric Nursing Practice - 6:30am
        }
        <input type="time" id="appt" name="appt"
        min="07:00" max="21:00" required
        onChange={this.userTimeHandler}
        value={this.state.userTime}
        onClick={this.validTimeHandler}
        />
        <button className='OrderButton' 
          onChange={console}
          disabled={!(this.state.submitableD && this.state.submitableT)}>Submit</button>
          {//!submittableT && submitableD 
          }

        <ValidTime Time={this.state.userTime} />
        
      </div>
    )
  }

}

export default App;
