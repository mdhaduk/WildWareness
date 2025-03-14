/**
 * Custom Jest resolver to handle React 19 compatibility
 * This resolver helps maintain compatibility between React 19 and testing libraries
 * that expect React 18 or earlier
 */

module.exports = (path, options) => {
  // Call the default resolver
  return options.defaultResolver(path, {
    ...options,
    // Make sure to properly resolve React packages
    packageFilter: pkg => {
      // For testing-library and related packages that expect React 18
      if (pkg.name === '@testing-library/react' || 
          pkg.name === '@testing-library/react-hooks' ||
          pkg.name === 'react-test-renderer') {
        // Ensure these packages use the available React version
        if (pkg.peerDependencies) {
          delete pkg.peerDependencies.react;
          delete pkg.peerDependencies['react-dom'];
        }
      }
      return pkg;
    },
  });
}; 