// import React from "react";
import React, { Component, PropTypes } from 'react';
// import PropTypes from 'prop-types';
// import Label from './label';
// import Redirection from './redirection';
import ReactTable from "react-table";
import Select from 'react-select';
// import { Link } from 'react-router-3';
import { Redirect } from 'react-router';
import { history } from './routes';
import ReactTooltip from 'react-tooltip';
// import { withRouter } from 'react-router-dom'
// import VirtualizedSelect from 'react-virtualized-select';
import Checkbox from 'rc-checkbox';

export default class Selection extends React.Component {
  constructor(props) {
    super(props);
    console.log("select ctor");
    this.handleSubmit = this.handleSubmit.bind(this);
    this.toggleCheckbox = this.toggleCheckbox.bind(this);
    this.toggleRadio = this.toggleRadio.bind(this);
    this.state = {
      redirect: false,
      setted: false,
      attribute_options: [],
      widget_options: [
        { label: "Correlations", value: 1 },
        { label: "Functional Dependencies", value: 2 },
        { label: "Association Rules", value: 3 },
        { label: "Maximal Uncovered Patterns", value: 4 },
      ],
      topk_options_multi: [
        { label: "Only show metadata", value: 0 },
        { label: "Top 1 widget", value: 1 },
        { label: "Top 2 widgets", value: 2 },
        { label: "Top 3 widgets", value: 3 },
        { label: "Top 4 widgets", value: 4 },
      ],
      topk_options_single: [
        { label: "Only show metadata", value:0 },
        { label: "Top 1 widget", value: 1 },
        { label: "Top 2 widgets", value: 2 },
      ],

      tmp_attribute_currentValues:[],
      tmp_protected_currentValues:[],
      str_colnames: {},

      protected_currentValues: [],
      label_currentValues: [],

      is_manually_widgets: true,
      widget_currentValues: [{ label: "Correlations", value: 1 },{ label: "Functional Dependencies", value: 2 },{ label: "Association Rules", value: 3 },
      { label: "Maximal Uncovered Patterns", value: 4 }],

      chose_numeric: false,
      num_widgets:0,

      attribute_currentValues: [],
      is_single_column: false,
      is_multi_column: true,
      is_whole: true,
      is_choose_attributes: false,

      is_query: false,
      query_currentValues: [],
      query_rangeValues: {},
      show_profit:false,

      has_fd: true,
    }
  }
  componentDidMount() {
    console.log("sel mount");

    fetch('/api/get_colnames/', { credentials: 'same-origin' })
      .then((response) => {
        // console.log("home then");
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // console.log("home data");
        if (false) {
          if (performance.navigation.type === 2) {
            this.setState({
              next: history.state.next,
              results: history.state.results,
              seted: true,
            });
          } else {
            this.setState({
              next: data.next,
              results: data.results,
              setted: true,
            });
            history.replaceState(this.state, null, '/');
          }
        } else {

          let tmp = this.state
          // console.log(data)

          if(data.is_demo){
            // console.log(data.is_demo);
            tmp["is_whole"]=false
            tmp["is_choose_attributes"]=true
            tmp["tmp_attribute_currentValues"] = [{ label: "decile_score", value: 9 },
            { label: "Violence_score", value: 54 },{ label: "event", value: 55 } ,{ label: "c_charge_degree", value: 56 },{ label: "first_name", value: 57 },{ label: "age", value: 58 }, { label: "marriage_status", value: 59 }]
            tmp["attribute_currentValues"] = [{ label: "decile_score", value: 9 },
            { label: "Violence_score", value: 54 },{ label: "event", value: 55 } ,{ label: "c_charge_degree", value: 56 },{ label: "first_name", value: 57 },{ label: "age", value: 58 }, { label: "marriage_status", value: 59 }]
            
            tmp["tmp_protected_currentValues"] =  [{ label: "sex", value: 50 },{ label: "race", value: 51 }]
            tmp["protected_currentValues"] = [{ label: "sex", value: 50 },{ label: "race", value: 51 }]
            
          }
          
        //also get params



          tmp["repr"] = data.repr;
          tmp["repr_names"] = data.repr_names;
          
          tmp["setted"] = true;
          for (let i = 0; i < data.colnames.length; i++) {
            tmp.attribute_options.push({ label: data.colnames[i], value: i });
          }
          for (let i = 0; i < data.str_colnames.length; i++) {
            tmp["str_colnames"][data.str_colnames[i]] = 0;
          }
          

          // console.log("didmount");
          // console.log(tmp);
          // console.log("setted");
          this.setState(tmp);
          // console.log(this.state);
        }
      })
      .catch(error => console.log(error));// eslint-disable-line no-console
  }

  // handleChange (selectedOption) {
  //   let tmp=this.state;
  //   tmp.currentValues.push(selectedOption);
  //   this.setState(tmp);
  // }

  handleSubmit(e) {

    event.preventDefault();
    const name = e.target.name;
    const checked = e.target.checked;
    let tmp = this.state;
    if (tmp["is_single_column"] && tmp["protected_currentValues"].length <= 0) {
      return (-1);
    }
    tmp[name] = !tmp[name]

    // str column_name
    if (tmp["is_single_column"] && Object.keys(tmp["protected_currentValues"]).length >= 1) {
      if (Object.keys(tmp["str_colnames"]).length === 0 || !(tmp["protected_currentValues"]['label'] in tmp["str_colnames"])) {
        tmp["chose_numeric"] = true;
      }
    }
    tmp["redirect"] = true;
    fetch('/api/form_submit/', {
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      method: ['POST'],
      body: JSON.stringify(this.state),
    }).then((response) => {
    })
      
    // fetch('/api/get_colnames/', { credentials: 'same-origin' })
    //   .then((response) => {

    //   })


    // fetch('/api/sel/', {
    //   credentials: 'same-origin',
    //   method: ['GET'],
    // }).then((res) => {
    //   console.log("sel res", res.sel);
    //   tmp = res.sel;

    // })
    console.log("out of fetch");

    this.setState(tmp);

    history.push({
      pathname: '/label',
      state: tmp
    })

    // console.log("s fetch post");
    // this.setState(tmp);
    // history.push('/label');
    // console.log("e fetch post");
  }

  toggleCheckbox(e) {
    console.log("sel s toggle");
    const name = e.target.name;
    const checked = e.target.checked;
    let tmp = this.state;
    tmp[name] = !tmp[name]
    if (name == "is_whole") {
      tmp["is_choose_attributes"] = !tmp["is_choose_attributes"]
    } else if (name == "is_choose_attributes") {
      tmp["is_whole"] = !tmp["is_whole"]

    } else if (name == "is_single_column") {
      tmp["widget_currentValues"] = [{ label: "Correlations", value: 1 },{ label: "Functional Dependencies", value: 2 }]
      tmp["is_multi_column"] = !tmp["is_multi_column"]
      tmp["is_manually_widgets"]=true
      tmp["protected_currentValues"]=[]
    } else if (name == "is_multi_column") {
      tmp["widget_currentValues"] = [{ label: "Correlations", value: 1 },
      { label: "Maximal Uncovered Patterns", value: 4 },]
      tmp["is_manually_widgets"]=true
      tmp["is_single_column"] = !tmp["is_single_column"]
      tmp["protected_currentValues"]=tmp["tmp_protected_currentValues"]
    }
    this.setState(tmp);
  }

  toggleRadio(value) {
    // console.log("cur val", value);

    const name = value;
    let tmp = this.state;
    tmp[name] = !tmp[name]
    if (name == "is_whole") {
      tmp["is_choose_attributes"] = !tmp["is_choose_attributes"]
    } else if (name == "is_choose_attributes") {
      tmp["is_whole"] = !tmp["is_whole"]
    } else if (name == "is_single_column") {
      tmp["is_multi_column"] = !tmp["is_multi_column"]
    } else if (name == "is_multi_column") {
      tmp["is_single_column"] = !tmp["is_single_column"]
    }
    this.setState(tmp);
    // console.log("tmp", tmp);

  }

  render() {
    if (this.state.redirect) {
      const { from } = this.props.location.state || '/';
      return (
        <div>
          {this.state.redirect && (
            <Redirect to={'/label'} />
          )}
        </div>
      )
    }
    if (!this.state.setted) {
      return ("");
    }
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

    let data = this.state.repr;
    let columns = this.state.repr_names.map((name) => {
      return (
        {
          Header: name,
          id: name,
          accessor: d => d[name],
        }
      );
    }
    );
    return (
      <div>
        <ReactTooltip />
        <form onSubmit={this.handleSubmit}>
          <div className="scontainer"></div>
          <div className="bcontainer">
            {/* <h2>Selections</h2> */}
            <div><div style={{ display: "inline-block", fontSize: "36px" }}><strong>Selections</strong></div>
                </div>
                <br/>
             <div style={{ display: "inline-block", fontSize: "6px"  }}><button style={{ fontSize: "10pt"  }} className="registerbtn" onClick={(e) => {
              e.preventDefault();
              let tmp = this.state;
              tmp["show_profit"]=!tmp["show_profit"]
              this.setState(tmp);
            }}>{!this.state.show_profit?"Show":"Hide"} profit table</button></div>&nbsp;&nbsp;&nbsp;
            <span data-tip="If 'Pick widgets yourself' is not checked, the system will return optimal widgets based on the profit table" className="ttip">
                <strong>?</strong></span>
            
            {this.state.show_profit?<div>
              <ReactTable
              data={this.state.repr}
              columns={columns}
              showPagination={false}
              defaultPageSize={4}
              className="-striped -highlight"
            />
            </div>:""}
            
<div></div>
            <span>
              <label>
                <input className="form-radio" type="radio" name="is_single_column" checked={this.state.is_single_column} onChange={this.toggleCheckbox} />
                <span className="checkbox-label" >Single Column Analysis <div style={{ display: "inline-block" }}><span data-tip="Must choose one attribute" className="warningtip1"><strong>{this.state.is_single_column ? <span>*</span>: ""}</strong></span></div>  </span>
                
                
              </label>
              <label className="container">
                <input className="form-radio" type="radio" name="is_multi_column" checked={this.state.is_multi_column} onChange={this.toggleCheckbox} />
                <span className="checkbox-label" >Multi-Column Analysis</span>
              </label>

              <span data-tip="Single Column Analysis will perform analysis on a attribute you select from the dropdown menu, while Multi-Column Analysis perform anaysis on combination of protected and other attributes you select below" className="ttip">
                <strong>?</strong></span>
            </span>



            {this.state.is_single_column ?
              <div>
                <div style={{ height: "3px" }}>&nbsp;</div>
                <Select
                  required={this.state.is_single_column}
                  closeMenuOnSelect={true}
                  components={{ ClearIndicator }}
                  styles={{ clearIndicator: ClearIndicatorStyles }}
                  defaultValue={[]}
                  onChange={(opt) => {
                    let tmp = this.state;
                    tmp.protected_currentValues = opt;
                    // console.log("protecte  d_currentValues");
                    this.setState(tmp);
                  }
                  }
                  simpleValue
                  options={this.state.attribute_options} />
              </div> : ""}
            {true ?
              <div>
              
                <span>
                  <label className="checkbox">
                    <input type="radio" className="form-radio" name="is_choose_attributes" checked={this.state.is_choose_attributes} onChange={this.toggleCheckbox} />
                    <span className="checkbox-label">Pick attributes</span>
                  </label>
                  &nbsp;&nbsp;&nbsp;
                    <label className="checkbox">
                    <input type="radio" className="form-radio" name="is_whole" checked={this.state.is_whole} onChange={this.toggleCheckbox} />
                    <span className="checkbox-label">Use all attributes</span>
                  </label>&nbsp;
              <span data-tip="Pick the columns you would like to be included in the analysis, or simply use all columns" className="ttip">
                    <strong>?</strong></span>
                  &nbsp;
              <span data-tip="If you pick many columns (i.e. more than 10 for a large dataset), we will sample rows when computing widgets such as association rules, as otherwise it takes huge amount of time" className="warningtip">
                    <strong>warning</strong></span>
                </span>
                
                {this.state.is_choose_attributes ? <div>
                  <div style={{ height: "3px" }}>&nbsp;</div>
                  <Select
                    required={this.state.is_multi_column && this.state.is_choose_attributes}
                    closeMenuOnSelect={false}
                    components={{ ClearIndicator }}
                    styles={{ clearIndicator: ClearIndicatorStyles }}
                    defaultValue={this.state.tmp_attribute_currentValues}
                    isMulti
                    onChange={(opt) => {
                      let tmp = this.state;
                      tmp.attribute_currentValues = opt
                      this.setState(tmp);
                    }
                    }
                    simpleValue
                    options={this.state.attribute_options} />
                </div> : ""
                }
                
                {/* <hr /> */}
              </div> : ""}


            {!this.state.is_single_column ? <div>
            <br />
              <ReactTooltip />
              <span >Pick protected/label attributes</span>
              &nbsp;
              <span data-tip="Protected attributes are the columns that potentially introduce biases against certain social groups (i.e. gender, race, etc)" className="ttip">
                <strong>?</strong></span>

              <div>
                <Select
                  required
                  closeMenuOnSelect={false}
                  components={{ ClearIndicator }}
                  styles={{ clearIndicator: ClearIndicatorStyles }}
                  defaultValue={this.state.tmp_protected_currentValues}
                  isMulti
                  onChange={(opt) => {
                    let tmp = this.state;
                    tmp.protected_currentValues = opt
                    this.setState(tmp)
                  }
                  }
                  simpleValue
                  options={this.state.attribute_options} />
              </div>

              {/* <hr /> */}
            </div> : ""

            }



            {true ? <div>
            <br />

              <label className="checkbox" >
                &nbsp;
                <Checkbox name="is_manually_widgets" checked={this.state.is_manually_widgets} onChange={this.toggleCheckbox}>
                </Checkbox>
                &nbsp;&nbsp;
                <span className="checkbox-label">Pick widgets yourself</span>&nbsp;
                <span data-tip="Pick what you would like to be included in the nutritional label" className="ttip">
                  <strong>?</strong></span>
              </label>
            <br />

            </div> : ""
            }


            {!this.state.is_manually_widgets ?
            <div>
              <Select
                  required={!this.state.is_manually_widgets}
                  closeMenuOnSelect={true}
                  components={{ ClearIndicator }}
                  styles={{ clearIndicator: ClearIndicatorStyles }}
                  defaultValue={{ label: "Only show metadata", value: 0 }}
                  
                  onChange={(opt) => {
                    let tmp = this.state;
                    tmp.num_widgets = opt['value'];
                    // console.log("protecte  d_currentValues");
                    this.setState(tmp);
                  }
                  }
                  simpleValue
                  options={this.state.is_single_column? this.state.topk_options_single:this.state.topk_options_multi} />
            </div>:""
            }

            {!this.state.is_single_column && this.state.is_manually_widgets ?
              <div>
                <Select
                  required={!this.state.is_single_column && this.state.is_manually_widgets}
                  closeMenuOnSelect={false}
                  components={{ ClearIndicator }}
                  styles={{ clearIndicator: ClearIndicatorStyles }}
                  defaultValue={this.state.widget_currentValues}
                  isMulti
                  onChange={(opt) => {
                    let tmp = this.state;
                    tmp.widget_currentValues = opt
                    // console.log("widget_currentValues");
                    for (let i = 0; i < opt.length; ++i) {
                      if (opt[i]['label'] == "Functional Dependencies") {
                        tmp.has_fd = true;
                        break;
                      }
                    }
                    this.setState(tmp);
                  }
                  }
                  simpleValue
                  options={this.state.widget_options} />
              </div> : ""}
            {this.state.is_single_column && this.state.is_manually_widgets ?
              <div>
                <Select
                  required={this.state.is_single_column && this.state.is_manually_widgets}
                  closeMenuOnSelect={false}
                  components={{ ClearIndicator }}
                  styles={{ clearIndicator: ClearIndicatorStyles }}
                  defaultValue={this.state.widget_currentValues}
                  isMulti
                  onChange={(opt) => {
                    let tmp = this.state;
                    tmp.widget_currentValues = opt
                    for (let i = 0; i < opt.length; ++i) {
                      if (opt[i]['label'] == "Functional Dependencies") {
                        tmp.has_fd = true;
                        break;
                      }
                    }
                    this.setState(tmp);
                  }
                  }
                  simpleValue
                  options={[{ label: "Correlations", value: 1 },
                  { label: "Functional Dependencies", value: 2 }]} />
              </div> : ""}


            {/* <hr /> */}
            <br />
            <label className="checkbox">&nbsp;
              <Checkbox name="is_query" checked={this.state.is_query} onChange={this.toggleCheckbox}>
              </Checkbox>
              &nbsp;&nbsp;
              <span className="checkbox-label">Slice the dataset by value range</span>
              &nbsp;
              <span data-tip="Constrain the value range for selected attributes" className="ttip">
                <strong>?</strong></span>
            </label>

            {this.state.is_query ?
              <div>
                <Select
                  required={this.state.is_query}
                  closeMenuOnSelect={false}
                  components={{ ClearIndicator }}
                  styles={{ clearIndicator: ClearIndicatorStyles }}
                  defaultValue={[]}
                  isMulti
                  onChange={(opt) => {
                    // console.log("query current ", opt);
                    let tmp = this.state;
                    let len_new = opt.length;
                    let len_old = tmp.query_currentValues.length;
                    if (len_new < len_old) {
                      let val_to_del = [];
                      let indices_to_del = [];
                      for (let i = 0; i < len_old; ++i) {
                        let found = false;
                        let val1 = tmp.query_currentValues[i];
                        for (let val2 of opt) {
                          if (val2["label"] == val1["label"]) {
                            found = true;
                            break;
                          }
                        }
                        if (!found) {
                          val_to_del.push(val1["label"]);
                          indices_to_del.push(i);
                          // break;
                        }
                      }

                      for (let i = val_to_del.length - 1; i >= 0; --i) {
                        delete tmp.query_rangeValues[val_to_del[i]];
                        tmp.query_currentValues.splice(indices_to_del[i], 1);
                      }
                    } else if (len_new > len_old) {
                      for (let i = 0; i < len_new; ++i) {
                        let found = false;
                        let val2 = opt[i];
                        for (let val1 of tmp.query_currentValues) {
                          if (val2["label"] == val1["label"]) {
                            found = true;
                          }
                        }
                        if (!found) {
                          if (val2["label"] in this.state.str_colnames) {
                            tmp.query_rangeValues[val2["label"]] = "";
                          }
                          else tmp.query_rangeValues[val2["label"]] = [Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER];
                          tmp.query_currentValues = opt;
                          break;
                        }
                      }
                    }

                    this.setState(tmp);
                  }
                  }
                  simpleValue
                  options={this.state.attribute_options} />
                <div>
                  {
                    Object.entries(this.state.query_rangeValues).map(([key, value]) => {
                      if (key in this.state.str_colnames) {
                        return (<div key={key}>{key}:<input
                          type='text'
                          className='form-control'
                          value={value}
                          placeholder="put a string value"
                          onChange={(evt) => {
                            let tmp = this.state;
                            this.state.query_rangeValues[key] = String(evt.target.value);
                            this.setState(tmp);
                          }
                          }
                        /></div>)
                      }
                      return (
                        <div>
                          {key}: [&nbsp;
                            <input
                            type='number'
                            step="0.1"
                            placeholder="lower bound (inclusive)"
                            className='form-control'
                            value={value[0]}
                            onChange={(evt) => {
                              let tmp = this.state;
                              this.state.query_rangeValues[key][0] = evt.target.value;
                              this.setState(tmp);
                            }
                            }
                          />
                          ,&nbsp;
                            <input
                            type='number'
                            step="0.1"
                            placeholder="upper bound (inclusive)"
                            className='form-control'
                            value={value[1]}
                            onChange={(evt) => {
                              let tmp = this.state;
                              this.state.query_rangeValues[key][1] = evt.target.value;
                              this.setState(tmp);
                            }
                            }
                          />
                          &nbsp;]
                        </div>
                      )
                    }
                    )}
                </div>
              </div> : ""}
            <br />
            <br />
            <div style={{ fontSize: "12px", float: "right"   }}><button style={{ fontSize: "14pt"  }} type="submit" className="generatebtn">Generate</button></div>
            {/* <button type="submit" className="registerbtn2"> Generate </button> */}
            <div className="scontainer"></div>
          </div>
        </form>
      </div>
    )
  }
}
