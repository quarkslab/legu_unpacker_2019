#ifndef PY_LEGU_H_
#define PY_LEGU_H_

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
PYBIND11_DECLARE_HOLDER_TYPE(T, std::unique_ptr<T>);

#endif
