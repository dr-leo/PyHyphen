#define PY_SSIZE_T_CLEAN
#define Py_LIMITED_API 0x03070000 
#include "Python.h"
#include "structmember.h"
#include "hyphen.h"
#include "string.h"

/* String constants for calls of Py_Unicode_FromEncodedObject etc.*/
static const char unicode_errors[] = "strict";



/* is raised if hnj_hyphen returns an error while trying to hyphenate a word*/
static PyObject *ErrorObject;

/* ----------------------------------------------------- */

/* Declarations for objects of type hyphenator_ */

/* type object to store the hyphenation dictionary. Its only method is 'apply' which calls the
core function 'hnj_hyphenate2'' from the wrapped library 'hnj_hyphen-2.3' */
typedef struct {
    PyObject_HEAD
    HyphenDict *dict;
    int lmin, rmin, compound_lmin, compound_rmin;
} HyDictobject;


/* ---------------------------------------------------------------- */

static char HyDict_apply__doc__[] =
"SUMMARY:\n\
apply(word: unicode object, mode: int) -> hyphenated word (return type depends on value of mode)\n\n\
Note: 'hnj' should normally be called only from the convenience interface provided by\
the hyphen.hyphenator class.\n\n\
word: must be lower-cased to be hyphenated correctly. Through the flags in mode,\n\
        the caller can provide information on whether the word was originally capitalized, \n\
        lower-cased or upper-cased.  Capital letters are restored \n\
        according to the value of 'mode'. The encoded representation of 'word'\n\
        may have at most 100 bytes including the terminating '\0'.\n\
mode: the 3 least significant bits are interpreted as flags with the following meaning:\n\
        - mode & 1 = 0: return a string with '=' inserted at the hyphenation points\n\
        - mode & 1 = 1: return a list of lists of the form [before_hyphen, after_hyphen]\n\
        - mode & 2 = 1: return a capitalized word\n\
        - mode & 4 = 1: return an upper-cased word\n";

/* get a pointer to the nth 8-bit or UTF-8 character of the word */
/* This is required because some operations are done at utf8 string level. */
static char * hindex(char * word, int n, int utf8) {
    int j = 0;
    while (j < n) {
        j++;
        word++;
        while (utf8 && ((((unsigned char) *word) >> 6) == 2)) word++;
    }
    return word;
}


/* Depending on the value of 'mode', convert a  C string to PyUnicode, handle also
    capitalization and upper case words. */
static PyObject * prepare_result(char *word, char *encoding, unsigned char mode)
{
    PyObject *result, *temp;
    
    /* first convert the C string to unicode. */
    if (!(temp = PyUnicode_Decode(word, strlen(word), encoding, unicode_errors)))
        return NULL;
    if (mode & 4) { /* capitalize entire word */
    printf("calling upper on %s", word);
        if (!(result = PyObject_CallMethod(temp, "upper", NULL)))
        {
            printf("error in upper");
            Py_DECREF(temp);
            return NULL;
      };
        }
    else
    {
        if (mode & 2) { /* capitalize first letter */
        printf("calling title");
            if (!(result = PyObject_CallMethod(temp, "title", NULL)))
            {
                Py_DECREF(temp);
                return NULL;
        };
        }
        else
        { 
        /* return the word unchanged as unicode obj */
            return temp;
        }
    }
    /* Delete temp when it is not returned (see above */
    Py_DECREF(temp);
    /* return the uppercased or titlecased result as unicode obj */
    return result;
}


/* core function of the hyphenator_ object type */
static PyObject *
HyDict_apply(HyDictobject *self, PyObject *args)
{
    const char separator[] = "=";
    char  *hyphenated_word, *hyphens, *word_str;
    char ** rep = NULL;
    char r;
    int * pos = NULL;
    int * cut = NULL;
    unsigned char mode;
    unsigned int wd_size, i, j, k ;
    Py_ssize_t hyph_count;
    PyObject *result, *s1, *s2, *separator_u = NULL;
/* mode:
   bit0 === 1: return a tuple, otherwise a word with '=' inserted at the positions of possible hyphenations.
   bit1 == 1: word must be capitalized before returning
  bit2 == 1: entire word must be uppered before returning  */


    /* parse and check arguments */
    if (!PyArg_ParseTuple(args, "esb", &self->dict->cset, &word_str, &mode))
          return NULL;
    wd_size = strlen(word_str);
    if (wd_size >= MAX_CHARS)
    {
        PyErr_SetString(PyExc_ValueError, "Word to be hyphenated may have at most 100 characters.");
        PyMem_Free(word_str);
        return NULL;
    }

    /* allocate memory for the return values of the core function hnj_hyphenate3*/
    hyphens = (char *) PyMem_Malloc(wd_size + 5);
    hyphenated_word = (char *) PyMem_Malloc(wd_size * 3);
    /* now actually try the hyphenation*/
    if (hnj_hyphen_hyphenate3(self->dict, word_str, wd_size, hyphens,
        hyphenated_word, &rep, &pos, &cut,
        self->lmin, self->rmin, self->compound_lmin, self->compound_rmin))
    {
        PyMem_Free(hyphens);
        PyMem_Free(hyphenated_word);
        PyMem_Free(word_str);
        PyErr_SetString(ErrorObject, "Cannot hyphenate word.");
        return NULL;
    }
    /* Count possible hyphenations. This is done by checking bit 0 of each */
    /* char of 'hyphens' which is 0 if and only if the word can be hyphened */
    /* at that position. Then proceed to */
    /* the real work, i.d. returning a unicode object with inserted '=' at each */
    /* possible hyphenation, or return a list of lists of two unicode objects */
    /* representing a possible hyphenation each. Note that the string */
    /* is useful only in languages without non-standard hyphenation, as */
    /* the string could contain more than one replacement, whereas */
    /* we are only interested in one replacement at the hyphenation position */
    /* we choose. */
    /* If no hyphenations were found, a string with 0 inserted '=', i.e. the original word, */
    /* or an empty list (with 0 pairs) is returned. */
    hyph_count = 0;
    for (i=0; (i+1) < strlen(hyphens); i++)
    {
        if (hyphens[i] & 1) hyph_count++;
    }
    /* Do we need to return a string with inserted '=', or a list of pairs? */
    if (!(mode & 1))
    {
        /* Prepare for returning a unicode obj of the form 'before_hyphen=after_hyphen.  */
        if (!(result = prepare_result(hyphenated_word, self->dict->cset, mode)))
        {
            PyMem_Free(hyphenated_word);
            PyMem_Free(word_str);
            PyMem_Free(hyphens);
            return NULL;
        }
        PyMem_Free(hyphenated_word);
    }
    else
    {
    PyMem_Free(hyphenated_word);
        /* construct a list of lists of two unicode objects. Each inner list */
        /* represents a possible hyphenation. */


        /* First create the outer list. Each element will be a list of two strings or unicode objects. */
        if (!(result = PyList_New(hyph_count)))
        {
            PyMem_Free(hyphens);
            PyMem_Free(word_str);
            return NULL;
        };
        /* now fill the resulting list from left to right with the pairs */
        j=0; hyph_count = 0;
        /* The following is needed to split the word (in which an '=' indicates the */
        /* hyphen position) */
        separator_u = PyUnicode_Decode(separator, 1, self->dict->cset, unicode_errors);
        for (i = 0; (i + 1) < strlen(word_str); i++)
        {
            /* i-th character utf8? Then just increment i */
            if (self->dict->utf8 && ((((unsigned char) word_str[i]) >> 6) == 2)) continue;

            /* Is here a hyphen? */
            if ((hyphens[j] & 1))
            {
                /* Build the hyphenated word at C string level. */
                /* first, handle non-standard hyphenation with replacement. */
                if (rep && rep[j])
                {
                    /* determine the position within word_str where to insert rep[j] */
                    /* do the replacement by appending the three substrings: */
                    hyphenated_word = (char *) PyMem_Malloc(strlen(word_str) + strlen(rep[j])+1);
                    k = hindex(word_str, j - pos[j] + 1, self->dict->utf8) - word_str;
                    r = word_str[k]; word_str[k] = 0;
                    strcpy(hyphenated_word, word_str);
                    strcat(hyphenated_word, rep[j]);
                    word_str[k] = r;
                    strcat(hyphenated_word, hindex(word_str + k, cut[j], self->dict->utf8));
                }
                else
                {
                    /* build the word in case of standard hyphenation. */
                    /* An '=' will be inserted so that the */
                    /* resulting string has the same format as in the non-standard case. */
                    hyphenated_word = (char *) PyMem_Malloc(strlen(word_str) + 2);
                    k = hindex(word_str, j + 1, self->dict->utf8) - word_str;
                    r = word_str[k]; word_str[k] = 0;
                    strcpy(hyphenated_word, word_str);
                    strcat(hyphenated_word, separator);
                    word_str[k] = r;
                    strcat(hyphenated_word, word_str + k);
                }
                /* Now prepare the resulting unicode object according to the value of mode */
                if (!(s1 = prepare_result(hyphenated_word, self->dict->cset, mode)))
                {
                    PyMem_Free(hyphenated_word);
                    PyMem_Free(hyphens);
                    PyMem_Free(word_str);
                    return NULL;
                }
                PyMem_Free(hyphenated_word);
                /* split it into two parts at the position of the '=' */
                /* and write the resulting list into the tuple */
                if (!((s2 = PyUnicode_Split(s1, separator_u, 1)) &&
                    (!PyList_SetItem(result, hyph_count++, s2))))
                {
                    Py_XDECREF(s2);
                    Py_DECREF(s1);
                    PyMem_Free(hyphens);
                    PyMem_Free(word_str);
                    return NULL;
                }
                Py_DECREF(s1);
            } /* finished with current hyphen */
            j++;
        } /* for loop*/
        Py_DECREF(separator_u);
    } /* end of else construct a list */
    PyMem_Free(hyphens);
    PyMem_Free(word_str);
    return result;
}


static struct PyMethodDef HyDict_methods[] = {
	{"apply",	(PyCFunction)HyDict_apply,	METH_VARARGS,	HyDict_apply__doc__},

	{NULL}		/* sentinel */
};

/* ---------- */



static void
HyDict_dealloc(HyDictobject *self)
{
	if (self->dict) hnj_hyphen_free(self->dict);
	PyObject_Del(self);
}

static int
HyDict_init(HyDictobject *self, PyObject *args) {

    /* Pointer to file-path of  dict */
    PyObject * fn;
    
    #if defined(_WIN32)
    const wchar_t * fn_ch;
#else
    const char * fn_ch;
 #endif
 
    if (!PyArg_ParseTuple(args, "O&iiii", PyUnicode_FSConverter, &fn,
    &self->lmin, &self->rmin, &self->compound_lmin, &self->compound_rmin))
	return -1;
    
      fn_ch = PyBytes_AsString(fn);
      printf("File path: %s .\n", fn_ch); 
      if (!(self->dict = hnj_hyphen_load(fn_ch)))
    {
          if (!PyErr_Occurred()) PyErr_SetString(PyExc_IOError, "Cannot load hyphen dictionary.");
          Py_DECREF(fn);
        return -1;
    }
    Py_DECREF(fn);
    return 0;
}


static char HyDict_type__doc__[] =
"Wrapper class for the hnj_hyphen library contained in this module.\n\n\
Usage: hyphenator_(dict_file_name: string)\n\
The init method will try to load a hyphenation dictionary with the filename passed.\n\
If an error occurs when trying to load the dictionary, IOError is raised.\n\
Dictionary files compatible with hnjmodule can be downloaded at the LibreOffice website.\n\n\
This class should normally be instantiated only by the convenience interface provided by\n\
the hyphen.hyphenator class.\n"
;



static PyType_Slot HyDict_type_slots[] = {
    {Py_tp_doc, HyDict_type__doc__},
    {Py_tp_dealloc, (destructor)HyDict_dealloc},
    {Py_tp_methods, HyDict_methods},
    {Py_tp_init, (initproc)HyDict_init},
    {Py_tp_free, },
};
static PyType_Spec HyDict_type_spec = {
    "hnjmodule.hyphenator_",
    sizeof(HyDictobject),
    0,
     Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    HyDict_type_slots,
};

/* ---------- */
/* ---------- */




/* End of code for hyphenator_ objects */
/* -------------------------------------------------------- */




static char module_doc[] =
"This C extension module is a wrapper around the hyphenation library 'hyphen-2.3.1' (2008-02-19).\n\
It should normally be imported and invoked only by the convenience interface provided\n\
by the hyphen.hyphenator class.\n"
;


static struct PyModuleDef hnjmodule = {
	PyModuleDef_HEAD_INIT,
	.m_name = "hnj",
	.m_doc = module_doc,
	.m_size = -1,
};

PyMODINIT_FUNC
PyInit_hnj(void)
{
	PyObject *m, *HyDict_type;

	

	/* Create the module and add the functions */
	m = PyModule_Create(&hnjmodule);
	if (m == NULL)
		goto fail;

	/* Add some symbolic constants to the module */
	if (ErrorObject == NULL) {
		ErrorObject = PyErr_NewException("hnj.error", NULL, NULL);
		if (ErrorObject == NULL)
			goto fail;
	}
	Py_INCREF(ErrorObject);
	PyModule_AddObject(m, "error", ErrorObject);

/* create HyDict_type */
if (!(HyDict_type = PyType_FromSpec(&HyDict_type_spec))) {
    goto fail;
};
Py_INCREF(HyDict_type);
    /* Add HiDict_type */
	if (PyModule_AddObject(m, "hyphenator_", HyDict_type) < 0) {
        Py_DECREF(HyDict_type);
        goto fail;
    }


	return m;
 fail:
 Py_DECREF(ErrorObject);
	Py_XDECREF(m);
	return NULL;
}

