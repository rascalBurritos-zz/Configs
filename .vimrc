set nocompatible
filetype off

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
    Plugin 'VundleVim/Vundle.vim'
    Plugin 'morhetz/gruvbox'
    Plugin 'vim-airline/vim-airline'
    Plugin 'vim-airline/vim-airline-themes'
    Plugin 'tpope/vim-commentary'
call vundle#end()            " required
filetype plugin indent on    " required
autocmd vimenter * ++nested colorscheme gruvbox

"all mode maps
noremap <C-L> <C-W><C-L>
noremap <C-s> :w<Enter>

"visual remaps
vnoremap <C-c> "+y
vnoremap <C-p> "+p

set mouse=a

" Line numbers
set relativenumber
set nu

set t_Co=256
set nowrap

"Prevent from C-D to bottom of screen
set scrolloff=6


" tab settings
set expandtab
set tabstop=4
set shiftwidth=4
set smartindent


"annoying timeout for esc
:set noesckeys
set timeoutlen=1000 ttimeoutlen=0

set background=dark
let g:airline_powerline_fonts = 1
" let g:airline_theme='gruvbox'
let g:airline_theme='gruvbox'
