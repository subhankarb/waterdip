import { ReactNode } from 'react';
import { isString } from 'lodash';
// material
import { Typography, Link, Grid, Box } from '@material-ui/core';
//
import { MBreadcrumbsProps } from './@material-extend/MBreadcrumbs';

// ----------------------------------------------------------------------

interface HeaderBreadcrumbsProps extends MBreadcrumbsProps {
  action?: ReactNode;
  heading: string;
  moreLink?: string | string[];
}

export default function HeaderBreadcrumbs({
  links,
  action,
  heading,
  moreLink = '' || [],
  sx,
  ...other
}: HeaderBreadcrumbsProps) {
  return (
    <Box sx={{ paddingBottom: '60px' }}>
      <Box
        sx={{
          ...sx,
          boxShadow: 4,
          width: '100%',
          background: '#fff',
          zIndex: 1,
          position: 'fixed',
          height: 'auto'
        }}
      >
        <Grid container spacing={2} justifyContent='space-between' sx={{ height: 'auto' }}>
          <Grid item xs={12} sm={6} sx={{ height: '60px' }}>
            <Box sx={{ display: 'flex', marginLeft: '20px', height: '60px', alignItems: 'center' }}>
              {links.map((data) => (
                <>
                  <Link
                    href={data.href}
                    style={{
                      fontFamily: 'Poppins',
                      fontStyle: 'normal',
                      fontWeight: 400,
                      fontSize: '16px',
                      lineHeight: '21px',
                      color: '#90A0B7'
                    }}
                  >
                    {data.name}
                  </Link>
                  <div
                    style={{
                      fontWeight: 400,
                      fontSize: '13px',
                      color: '#90A0B7',
                      paddingLeft: '4px',
                      paddingRight: '4px'
                    }}
                  >
                    {' '}
                    /{' '}
                  </div>
                </>
              ))}

              <div
                style={{
                  fontFamily: 'Poppins',
                  fontStyle: 'normal',
                  fontWeight: 500,
                  fontSize: '16px',
                  lineHeight: '21px',
                  /* identical to box height */

                  color: '#2A2A2A'
                }}
              >
                {heading}
              </div>
            </Box>
          </Grid>
          {/* <Grid item xs={3} sx={{ height: '60px' }} /> */}
          {action && 
            <Grid item xs={12} sm={6} lg={4} sx={{ height: '60px' }}>
              <Box sx={{ display: 'flex', marginLeft: '20px', height: '60px'}}>{action && <Box>{action}</Box>}</Box>
            </Grid>
          }
          
        </Grid>

        <Box sx={{ mt: 2 }}>
          {isString(moreLink) ? (
            <Link href={moreLink} target="_blank" variant="body2">
              {moreLink}
            </Link>
          ) : (
            moreLink.map((href) => (
              <Link
                noWrap
                key={href}
                href={href}
                variant="body2"
                target="_blank"
                sx={{ display: 'table' }}
              >
                {href}
              </Link>
            ))
          )}
        </Box>
      </Box>
    </Box>
  );
}
