export default function (req, res, next) {
  res.ok = function (data, message) {
    const response = {
      success: true,
      message: message || "Operation successfully executed.",
      data: data,
    };
    res.status(200);
    res.json(response);
  };
  res.error = function (data, message) {
    const response = {
      code: "OK",
      message:
        message && message.message ? message.message : "Something went wrong",
      data: data,
    };
    res.status(200);
    res.json(response);
  };
  res.badRequest = function (data, message) {
    const response = {
      code: "E_BAD_REQUEST",
      message: message || "Bad request",
      data: data || {},
    };
    res.status(400);
    res.json(response);
  };
  res.notAccess = function (data, message) {
    const response = {
      code: "E_BAD_REQUEST",
      message: message || "Bad request",
      data: data || {},
    };
    res.status(403);
    res.json(response);
  };
  res.serverError = function (data, message) {
    const response = {
      code: "E_SERVER_ERROR",
      message: message || "Something went wrong",
      data: data || {},
    };
    res.status(500);
    res.json(response);
  };
  res.unAuthorized = function (data, message) {
    const response = {
      code: "E_UNAUTHORIZED",
      message: message,
      data: data || {},
    };
    res.status(401);
    res.json(response);
  };
  next();
}
