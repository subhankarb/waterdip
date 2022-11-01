// material
import { Grid, Card, Container, CardContent, Typography } from '@material-ui/core';
// components
import Page from '../components/Page';
import CopyClipboard from '../components/CopyClipboard';
import HeaderBreadcrumbs from '../components/HeaderBreadcrumbs';

// ----------------------------------------------------------------------

export default function Keys() {
  return (
    <Page title="API Keys | Waterdip">
      <Container maxWidth="lg">
        <HeaderBreadcrumbs heading="API Keys" links={[{ name: 'API Key List' }]} />
        <Grid container spacing={3}>
          <Grid item xs={12} md={12} lg={12}>
            <Card sx={{ display: 'flex', alignItems: 'center', p: 3 }}>
              <CardContent>
                <Typography variant="h5" display="flex" noWrap={true}>
                  Admin Key
                </Typography>
                <Typography display="flex" noWrap={true}>
                  Generated on 9th June
                </Typography>
              </CardContent>
              <CopyClipboard value="9d5da59s-4bfa-3412-c413-8bccc25549e1" />
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Page>
  );
}
