import React from 'react';
import Select from 'material-ui/Select';
import { FormControl } from 'material-ui/Form';
import { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => ({
  select: {
    width: '600px'
  }
});

class ChartOptions extends React.Component {
  constructor(props) {
    super(props);
    this.state = { topicId: 0 };
  }

  render() {
    const { classes } = this.props;

    const topicMenuItems = this.props.topics.map((e) => {
      return <MenuItem key={e.id} value={e.id}>{e.name}</MenuItem>;
    });

    return (
      <div>
        <form>
          <FormControl>
            <InputLabel>Topic</InputLabel>
            <Select
              className={classes.select}
              value={this.state.topicId}
              onChange={this.handleSelectChange.bind(this)}>
              {topicMenuItems}
            </Select>
          </FormControl>
        </form>
      </div>
    );
  }

  handleSelectChange(event) {
    this.setState({ topicId: event.target.value });
  }
}

export default withStyles(styles)(ChartOptions);
