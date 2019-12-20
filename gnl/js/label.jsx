import React from 'react';
// import PropTypes from 'prop-types';
// import ReactDOM from 'react-dom';
import MultiBasic from './multi_basic';
// import Correlation from './correlation';
import FunctionalDependency from './functional_dependency';
import AssociationRule from './association_rule';
// import SingleColumn from './single_column';
// import Coverage from './coverage';
import Select from 'react-select';
import {HorizontalBar} from 'react-chartjs-2';
import ReactTable from "react-table";
import { HashLink as Link } from 'react-router-hash-link';
import $ from 'jquery';
export default class Label extends React.Component {
  constructor(props) {
    super(props);
    console.log("label ctor");
    this.handleClick = this.handleClick.bind(this);
    // this.setParams = this.setParams.bind(this);
    // this.handleRemove = this.handleRemove.bind(this);
    let widget_currentValues = this.props["location"]["state"]['widget_currentValues'];
    let protected_currentValues = this.props["location"]["state"]['protected_currentValues'];
    // let added_widgets=[];
    this.state = {
      setted: false,
      widget_currentValues: this.props["location"]["state"]['widget_currentValues'],
      widget_options: [
        { label: "Correlations", value: 1 },
        { label: "Functional Dependencies", value: 2 },
        { label: "Association Rules", value: 3 },
        { label: "Maximal Uncovered Patterns", value: 4 },
      ],
      // cur_widget_names=["Correlations","Association Rules"],
      // cur_widgets=[],
      additional: [],
      chose_numeric: this.props["location"]["state"]['chose_numeric'],
      has_Correlation: false,
      has_FunctionalDependency: false,
      has_AssociationRule: false,
      has_Coverage: false,
      has_SingleColumn: this.props["location"]["state"]['is_single_column'],
      dataa:{},
      labels:[],
      values:[],
      single_colname:"Column Name",
      no_numeric:false
      //this.props["location"]["state"]['is_single_column']
    }
    // console.log("chose is ");
    // console.log(this.state['chose_numeric']);
    // console.log("single is ", this.props["location"]["state"]['is_single_column']);



    // console.log("label widget_currentValues", widget_currentValues);


    if (this.props["location"]["state"]["is_manually_widgets"]) {
      for (let i = 0; i < widget_currentValues.length; ++i) {
        if (widget_currentValues[i]['value'] == 1) {
          this.state['has_Correlation'] = true;
        } else if (widget_currentValues[i]['value'] == 2) {
          this.state['has_FunctionalDependency'] = true;
        } else if (widget_currentValues[i]['value'] == 3) {
          this.state['has_AssociationRule'] = true;
        } else if (widget_currentValues[i]['value'] == 4) {
          this.state['has_Coverage'] = true;
        }
      }
    }


    // if (!this.props["location"]["state"]["is_manually_widgets"]) {
    //   this.state = {
    //     setted: false,
    //     widget_currentValues: [{ label: "Correlations", value: 1 },
    //     { label: "Functional Dependencies", value: 2 },
    //     { label: "Association Rules", value: 3 },
    //     { label: "Maximal Uncovered Patterns", value: 4 }],
    //     widget_options: [
    //       { label: "Correlation", value: 1 },
    //       { label: "Functional Dependencies", value: 2 },
    //       { label: "Association Rules", value: 3 },
    //       { label: "Maximal Uncovered Patterns", value: 4 },
    //     ],
    //     additional: [],
    //     chose_numeric: this.props["location"]["state"]['chose_numeric'],
    //     has_Correlation: true,
    //     has_FunctionalDependency: true,
    //     has_AssociationRule: true,
    //     has_Coverage: true,
    //     has_SingleColumn: this.props["location"]["state"]['is_single_column'],
    //   }
    // }


    // if (protected_currentValues.length == 0) {
    //   console.log("here");
    //   this.state['has_Correlation'] = false;
    // }
    if (this.state['has_SingleColumn']) {
      this.state['widget_options'] = [

        { label: "Functional Dependencies", value: 2 }
      ]
      if (protected_currentValues.length != 0) this.state["widget_options"].push({ label: "Correlations", value: 1 })
    }
  }

  // setParams() {

  //   fetch('/api/params/', {
  //     credentials: 'same-origin',
  //     headers: { 'Content-Type': 'application/json' },
  //     method: ['POST'],
  //     body: JSON.stringify(this.state),
  //   }).then((res) => {

  //   })
  // }
  handleClick(e) {
    e.preventDefault();
    let tmp = this.state;
    let i = 0;
    let added_topk = false;
    let added_coverage = false;
    let added_fd = false;
    let added_ar = false;
    for (; i < tmp["widget_currentValues"].length; i++) {
      if (tmp["widget_currentValues"][i]["label"] == "Correlations") {
        if (!tmp['has_Correlation']) added_topk = true;
        tmp['has_Correlation'] = true;
      }
      else if (tmp["widget_currentValues"][i]["label"] == "Functional Dependencies") {
        if (!tmp['has_FunctionalDependency']) added_fd = true;
        tmp['has_FunctionalDependency'] = true;
      }
      else if (tmp["widget_currentValues"][i]["label"] == "Association Rules") {
        if (!tmp['has_AssociationRule']) added_ar = true;
        tmp['has_AssociationRule'] = true;
      }
      else {
        if (!tmp['has_Coverage']) added_coverage = true;
        tmp['has_Coverage'] = true;
      }
    }
    fetch('/api/params/', {
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      method: ['POST'],
      body: JSON.stringify(tmp),
    })
    console.log("set new widgets");
    // if (!tmp["has_SingleColumn"] && added_coverage) {
    //   $(this.refs.reference).html(
    //     loadJson("mups.json")
    //   );
    // }
    // if (tmp["has_SingleColumn"]) {
    //   console.log("in mount single col");
    //   $(this.refs.reference).html(
    //     load_single_meta()
    //   );
    // }
    if (added_fd || added_topk) {
      console.log("added cor");
      $(this.refs.reference).html(
        load_correlation()
      );
    }
    if (added_coverage) {
      console.log("added cor");
      $(this.refs.reference).html(
        load_mups()
      );
    }
    this.setState(tmp)
  }


  componentDidMount() {
    // var today = new Date();
    // var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    // console.log("label mount", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds())
    let tmp = this.state;

    fetch('/api/sel/', { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log("res sel", data);
        if(tmp["has_SingleColumn"] && !tmp["chose_numeric"]){
          tmp["values"]=data.values
          tmp["labels"]=data.labels
          tmp["single_colname"]=data.single_colname
        }
        tmp['no_numeric']=data.no_numeric
        console.log("Im here");
        
        console.log(data.no_numeric);
        


        if (!this.props["location"]["state"]["is_manually_widgets"]) {
          tmp["has_Correlation"] = false
          tmp["has_FunctionalDependency"] = false
          tmp["has_AssociationRule"] = false
          tmp["has_Coverage"] = false
          tmp["widget_currentValues"] = data.sel
          for (let i = 0; i < data.sel.length; ++i) {
            let cur = data.sel[i];
            if (cur["label"] == "Correlations") {
              tmp["has_Correlation"] = true;
            }
            else if (cur["label"] == "Functional Dependencies") {
              tmp["has_FunctionalDependency"] = true;
            }
            else if (cur["label"] == "Association Rules") {
              tmp["has_AssociationRule"] = true;
            }
            else if (cur["label"] == "Maximal Uncovered Patterns") {
              tmp["has_Coverage"] = true;
            }
          }
        }
        // console.log(data.sel);

        if (tmp["has_SingleColumn"]&&tmp["chose_numeric"]) {
          // console.log("in mount single col");
          $(this.refs.reference).html(
            load_single_meta()
          );
        }
        if (tmp["has_Correlation"]) {
          // console.log("in mount cor");
          $(this.refs.reference).html(
            load_correlation()
          );
        }
        if (tmp["has_Coverage"]) {
          // console.log("in mount cor");
          $(this.refs.reference).html(
            load_mups()
          );
        }
        tmp["setted"] = true;
        // this.setState(tmp);

        this.setState(tmp);
      }
      )
      .catch(error => console.log(error));// eslint-disable-line no-console

    // console.log("e label mount", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds());
  }
  render() {
    var today = new Date();
    // console.log("label render", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds())
    const CustomClearText = () => 'clear all';
    const ClearIndicator = (props) => {
      const { children = <CustomClearText />, getStyles, innerProps: { ref, ...restInnerProps } } = props;
      return (
        <div {...restInnerProps} ref={ref} style={getStyles('clearIndicator', props)}>
          <div style={{ padding: '0px 5px' }}>
            {children}
          </div>
        </div>
      );
    };
    const ClearIndicatorStyles = (base, state) => ({
      ...base,
      cursor: 'pointer',
      color: state.isFocused ? 'blue' : 'black',
    });

    const dataa = {
      labels: this.state.labels,
      datasets: [
        {
          label: this.state.single_colname,
          backgroundColor: 'rgba(0,0,0,1)',
          borderColor: 'rgba(119,119,119,1)',
          borderWidth: 1,
          hoverBackgroundColor: 'rgba(51,51,51,1)',
          hoverBorderColor: 'rgba(119,119,119,1)',
          data: this.state.values
        }
      ]
    };
    // const margin = {top: 20, right: 20, bottom: 30, left: 40};
    return (
      <div ref="reference">
        <div className="left_column">


          <div className="tab"><Link to="label#overview"># Data Overview</Link></div>
          {this.state.has_Correlation ? <div className="tab"><Link to="label#correlation"># Correlations</Link></div> : ""}
          {!this.state.has_SingleColumn && this.state.has_Coverage ? <div className="tab"><Link to="label#mups"># Maximal Uncovered Patterns</Link></div> : ""}
          {!this.state.has_SingleColumn && this.state.has_AssociationRule ? <div className="tab"><Link to="label#ars"># Association Rules</Link></div> : ""}
          {this.state.has_FunctionalDependency ? <div className="tab"><Link to="label#fds"># Functional Dependencies</Link></div> : ""}
          <div className="tab"><Link to="label#additional_widgets"># Generate More Labels</Link></div>
        </div>

        <div className="right_column">
          <div id="overview" className="vis">


                 
            <div style={{ display: "inline-block", fontSize: "32px" }}><strong>Data Overview </strong></div><div style={{ display: "inline-block", fontSize: "16px" }}>(Please wait while the widgets are rendering)</div><br />
            {this.state.has_SingleColumn && this.state.chose_numeric ?
              <div className="frame" id="ov">
                <div className="ov_row_head">
                  <span className="ov_cell attr">Attribute Name</span>
                  <span className="ov_cell hg">Histogram</span>
                  <span className="ov_cell max">Max</span>
                  <span className="ov_cell min">Min</span>
                  <span className="ov_cell mean">Mean</span>
                  <span className="ov_cell nul">Null Entries</span>
                  <span className="ov_cell uniq">Unique Entries</span>
                </div>
              </div> :
              ""
            }
            {this.state.has_SingleColumn && !this.state.chose_numeric ?
              <div className="frame" id="non">
                <HorizontalBar data={dataa} />
              </div>: ""
            }
            {!this.state.has_SingleColumn ?
              <div className="frame">
                <div className="ov_label_title">
                  <MultiBasic key={0} />
                </div>
              </div>
              : ""
            }
          </div>
          {this.state.has_Correlation ?
            (<div id="correlation" className="vis">
              <div><div style={{ display: "inline-block", fontSize: "32px" }}><strong>Correlations</strong></div>&nbsp;&nbsp;&nbsp;
              <div style={{ display: "inline-block", fontSize: "30px" }}><button className="rmv_button" onClick={(e) => {
                  e.preventDefault();
                  let tmp = this.state;
                  tmp["has_Correlation"] = false;
                  for (let i = 0; i < tmp["widget_currentValues"].length; ++i) {
                    if (tmp["widget_currentValues"][i]["label"] == "Correlations") {
                      tmp["widget_currentValues"].splice(i, 1);
                      break
                    }
                  }
                  fetch('/api/params/', {
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json' },
                    method: ['POST'],
                    body: JSON.stringify(tmp),
                  }).then((res) => {
                  })
                  this.setState(tmp);
                }}>X</button></div></div>
              <p>This shows correlation between selected <strong>ordinal</strong> attributes. Click on the squares to see scatterplot.</p>
              
              {this.state.no_numeric?<div>No numeric column selected</div>:""}
              
              <div className="frame">
                {this.state.no_numeric?<div>No numeric column selected</div>:""}
                <div id="diagramCorrelations" className='diagram'> </div>
                <h4 id="diagramScatterPlotName" className='diagram'></h4>
                <div id="diagramScatterPlot" className='diagram'> </div>
              </div>
            </div>) : ""
          }
          {!this.state.has_SingleColumn && this.state.has_Coverage ?
            (<div id="mups" className="vis">
              <div><div style={{ display: "inline-block", fontSize: "32px" }}><strong>Maximal Uncovered Patterns</strong></div>&nbsp;&nbsp;&nbsp;
              <div style={{ display: "inline-block" }}><button className="rmv_button" onClick={(e) => {
                  e.preventDefault();
                  let tmp = this.state;
                  tmp["has_Coverage"] = false;

                  for (let i = 0; i < tmp["widget_currentValues"].length; ++i) {
                    if (tmp["widget_currentValues"][i]["label"] == "Maximal Uncovered Patterns") {
                      tmp["widget_currentValues"].splice(i, 1);
                      break

                    }
                  }
                  fetch('/api/params/', {
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json' },
                    method: ['POST'],
                    body: JSON.stringify(tmp),
                  }).then((res) => {
                  })
                  this.setState(tmp);
                  // console.log("tmp", tmp);


                }}>X</button></div></div>
              <p>Maximal uncovered pattern shows the combination of values that are undersampled in the dataset</p>
              <div className="frame"><div id="mups_vis"></div></div>
            </div>) : ""
          }
          {!this.state.has_SingleColumn && this.state.has_AssociationRule ?
            (<div id="ars" className="vis">
              <div><div style={{ display: "inline-block", fontSize: "32px" }}><strong>Association Rules </strong></div>&nbsp;&nbsp;&nbsp;
              <div style={{ display: "inline-block" }}><button className="rmv_button" onClick={(e) => {
                  e.preventDefault();
                  let tmp = this.state;
                  tmp["has_AssociationRule"] = false;
                  // console.log("brefore ", tmp["widget_currentValues"]);
                  let tlist = tmp["widget_currentValues"]
                  // console.log("length is ", tlist.length);
                  
                  for (let i = 0; i < tlist.length; ++i) {
                    // console.log(i," ",tmp["widget_currentValues"][i]);
                    
                    if (tmp["widget_currentValues"][i]["label"] == "Association Rules") {
                      // console.log("here");
                      tmp["widget_currentValues"].splice(i, 1);
                      break
                    }
                  }
                  // console.log("after ", tmp["widget_currentValues"]);
                  
                  fetch('/api/params/', {
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json' },
                    method: ['POST'],
                    body: JSON.stringify(tmp),
                  }).then((res) => {
                  })
                  // this.setState(tmp);
                  // console.log("cur tmp", tmp["widget_currentValues"]);

                  this.setState(tmp);
                }}>X</button></div></div>
              <p style={{ color: "red" }}>WARNING: When there are many columns (i.e. >10 for large dataset), we will sample rows to reduce computation time</p>
              <p>Association rule of a dataset is a set of directed relations in between set A and set B such that values of set A determines the values of set B for over some predefined probability. You can drag the nodes around or magnify/diminish them by scrolling.</p>

              <div id="ars_vis" className="frame">
                <div>
                  <AssociationRule key={3} />
                </div>
              </div>
            </div>) : ""
          }
          {this.state.has_FunctionalDependency ?

            (<div id="fds" className="vis">
              <div><div style={{ display: "inline-block", fontSize: "32px" }}><strong>Functional Dependencies </strong></div>&nbsp;&nbsp;&nbsp;
              <div style={{ display: "inline-block" }}><button className="rmv_button" onClick={(e) => {

                  e.preventDefault();
                  let tmp = this.state;
                  tmp["has_FunctionalDependency"] = false;

                  for (let i = 0; i < tmp["widget_currentValues"].length; ++i) {
                    if (tmp["widget_currentValues"][i]["label"] == "Functional Dependencies") {
                      tmp["widget_currentValues"].splice(i, 1);
                      break

                    }
                  }
                  fetch('/api/params/', {
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json' },
                    method: ['POST'],
                    body: JSON.stringify(tmp),
                  }).then((res) => {
                  })
                  this.setState(tmp);
                }}>X</button></div>
              </div>
              <p style={{ color: "red" }}>WARNING: When there are many columns (i.e. >10 for large dataset), we will sample rows to reduce computation time </p>
              <p>Functional dependency is a relationship that exists when combinaton of attributes uniquely determines another attribute. You can drag the nodes around or magnify/diminish them by scrolling.</p>
              <div id="fd_vis" className="frame">
                <div>
                  <FunctionalDependency key={2} />
                </div>
              </div>
            </div>)
            : ""
          }
          <div id="additional_widgets" className="vis">
            <div style={{ fontSize: "32px" }}><strong>Generate More Labels</strong></div>
            <div>
              <div style={{ display: "inline-block", width: "95%" }}>
                {this.state.has_SingleColumn ? <div>
                  <Select
                    required
                    closeMenuOnSelect={false}
                    components={{ ClearIndicator }}
                    styles={{ clearIndicator: ClearIndicatorStyles }}
                    defaultValue={[]}
                    isMulti
                    onChange={(opt) => {
                      let tmp = this.state;
                      tmp.widget_currentValues = opt
                      this.setState(tmp);
                      // console.log("tmp", tmp);
                    }
                    }
                    simpleValue
                    options={[
                      { label: "Correlations", value: 1 },
                      { label: "Functional Dependencies", value: 2 },
                    ]} />
                </div> : <div>
                    <Select
                      required
                      closeMenuOnSelect={false}
                      components={{ ClearIndicator }}
                      styles={{ clearIndicator: ClearIndicatorStyles }}
                      defaultValue={[]}
                      isMulti
                      onChange={(opt) => {
                        let tmp = this.state;
                        tmp.widget_currentValues = opt
                        this.setState(tmp);
                        // console.log("tmp", tmp);

                      }
                      }
                      simpleValue
                      options={[
                        { label: "Correlations", value: 1 },
                        { label: "Functional Dependencies", value: 2 },
                        { label: "Association Rules", value: 3 },
                        { label: "Maximal Uncovered Patterns", value: 4 },
                      ]} />
                  </div>}

              </div>
              <div style={{ display: "inline-block", width: "5%" }}><button className="add_button" onClick={this.handleClick}>+</button></div>

            </div>
          </div>

        </div>

      </div>
    )
  }
}
// Label.propTypes = {
//   url: PropTypes.string.isRequired,
// };
