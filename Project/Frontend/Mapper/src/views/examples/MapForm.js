import React from 'react';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';

export default function MapForm() {
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Map Address
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            required
            id="streetName"
            name="streetName"
            label="Street name"
            fullWidth
            autoComplete="Rua"
          />
        </Grid>
        <Grid item xs={6} sm={3}>
            <TextField
            required
            id="beginingX"
            name="beginingX"
            label="X coord to start"
            fullWidth
            autoComplete="0"
            />
        </Grid>
        <Grid item xs={6} sm={3}>
            <TextField
            required
            id="beginingY"
            name="beginingY"
            label="Y coord to start"
            fullWidth
            autoComplete="0"
            />
        </Grid>
        <Grid item xs={6} sm={3}>
            <TextField
            required
            id="endingX"
            name="endingX"
            label="X coord to end"
            fullWidth
            autoComplete="1000"
            />
        </Grid>
        <Grid item xs={6} sm={3}>
            <TextField
            required
            id="endingY"
            name="endingY"
            label="Y coord to end"
            fullWidth
            autoComplete="100"
            />
        </Grid>
        <Grid item xs={12}>
          <TextField
            required
            id="city"
            name="city"
            label="City"
            fullWidth
            autoComplete="Cidade "
          />
        </Grid>
      </Grid>
    </React.Fragment>
  );
}