const catchAsync = (fn) => {
  return (req, res, next) => {
    fn(req, res, next).catch((err) => {
      if (err.errors) {
        let errorBag = [];
        Object.keys(err.errors).forEach((fieldName) => {
          errorBag.push({ [fieldName]: err.errors[fieldName] });
        });
        return res.badRequest(null, errorBag);
      } else {
        let errorMessage = {
          message: err.message,
        };
        if (err.isAxiosError) {
          errorMessage.data = {
            url: err.response.config.url,
            method: err.response.config.method,
            data: err.response.config.data,
            headers: err.response.config.headers,
          };
        }
        return res.badRequest(null, errorMessage);
      }
    });
  };
};
export default catchAsync;
