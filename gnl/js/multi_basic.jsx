import React from 'react';
// import PropTypes from 'prop-types';
// import ReactDOM from 'react-dom';
import ReactTable from "react-table";
import matchSorter from 'match-sorter';
// import {
//   withScreenSize,
// } from '@data-ui/histogram';


export default class MultiBasic extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      setted: false,
    }
  }

  componentDidMount() {
    fetch('/api/multi_basic/', { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        console.log('multi basic get data');
        // console.log("data.repr ", data.repr);

        this.setState({
          repr: data.repr,
          repr_names: data.repr_names,
          keywords: data.keywords,
          num_rows: data.num_rows,
          num_cols: data.num_cols,
          num_missing: data.num_missing,
          setted: true,
        });
      }
      )
      .catch(error => console.log(error));// eslint-disable-line no-console
  }
  render() {


    if (this.state.setted) {
      let data = this.state.repr;
      let columns = this.state.repr_names.map((name) => {
        return (
          {
            Header: name,
            id: name,
            accessor: d => d[name],
            filterMethod: (filter, rows) =>
              matchSorter(rows, filter.value, { keys: [name] }),
            filterAll: true
          }
        );
      }
      );
      // console.log("columns: ", columns);

      return (
        <div>
          <div className="ov_row_head">
            <span className="ov_cell mattr">Cardinality</span>
            <span className="ov_cell mattr">Feature Dimension</span>
            <span className="ov_cell mattr"># Missing Entries</span>
            <span className="ov_cell mmean">Keywords (sorted descendingly by frequency)</span>
          </div>
          <div className="ov_row">
            <span className="ov_cell mattr">{this.state.num_rows}</span>
            <span className="ov_cell mattr">{this.state.num_cols}</span>
            <span className="ov_cell mattr">{this.state.num_missing}</span>
            <span className="ov_cell mmean">{this.state.keywords.map((keyword, i) => {
              if (i == this.state.keywords.length - 1) {
                return (`${keyword}`)
              } else {
                return (`${keyword}, `)
              }
            })}</span>
          </div>
          <div className="ov_row_head">
            <span className="ov_cell mattr">Representative rows and columns</span>
          </div>
          <div className="ov_row">
            <ReactTable
              data={data}
              columns={columns}
              defaultPageSize={5}
              filterable
              defaultFilterMethod={(filter, row) =>
                String(row[filter.id]) === filter.value}

              className="-striped -highlight"
            />
          </div>


        </div>
      );

    }
    return ("");


  }
}
